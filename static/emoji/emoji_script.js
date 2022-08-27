const categories = new Map([
    ['People', ['People & Body', 'Smileys & Emotion', 'Component']],
    ['Nature', ['Animals & Nature']],
    ['Food', ['Food & Drink']],
    ['Activities', ['Activities']],
    ['Travel', ['Travel & Places']],
    ['Objects', ['Objects']],
    ['Symbols', ['Symbols']],
    ['Flags', ['Flags']],
    ['Custom', []]
]);

window.onload = function () {
    if (!window.jQuery) throw "jQuery not loaded - some features may broke";
    if (!Fuse) throw "Fuse lib not loaded - some features may broke";
}

class EmojiKeyboard {
    constructor() {
        this.emojis = new Map(Array.from(categories, v => [v[0], []])); // we take categories names with empty lists
        this.categories = Array.from(categories.keys());
        this.init_base_emojis();
        this.callback = (emoji, gotClosed) => {
        };
        this.auto_reconstruction = true;
        this.default_placeholder = "Find the right emoji for your needs 👌";
        this.resizable = true;
        this.fuseIndex = null;
        this.fuse = null;
        if ("IntersectionObserver" in window) {
            // https://dev.to/ekafyi/lazy-loading-images-with-vanilla-javascript-2fbj
            this.lazyImageObserver = new IntersectionObserver((entries, observer) => {
                // Loop through IntersectionObserverEntry objects
                entries.forEach(entry => {
                    // Do these if the target intersects with the root
                    if (entry.isIntersecting) {
                        let lazyImage = entry.target;
                        lazyImage.src = lazyImage.dataset.src;
                        lazyImage.classList.remove("lazy");
                        observer.unobserve(lazyImage);
                    }
                });
            });
            // https://stackoverflow.com/a/57991537/11213823
            this.stickyObserver = new IntersectionObserver(entries => {
                entries.forEach(entry => {
                    if (!entry.target.offsetParent) return;
                    const scrollPos = entry.target.offsetParent.scrollTop - entry.target.offsetTop;
                    if (scrollPos >= 1) {
                        const categ = entry.target.dataset.emojikb_categ;
                        const list = document.getElementById("emojikb-leftlist");
                        const targets = list.querySelectorAll('svg[data-emojikb_categ="' + categ + '"]');
                        if (!targets[0]) return;
                        this.click_on_category(this, targets[0], true);
                    }
                })
            }, {threshold: [0, 1]})
        }
    }

    instantiate(elem) {
        this.wait_for_ready().then(() => {
            // elem should be a button
            let document = elem.ownerDocument;
            this.get_keyboard(document); // create keyboard if needed
            elem.addEventListener("click", () => this.toggle_window());
        })
    }

    toggle_window() {
        let kb = document.getElementById("emojikb-maindiv");
        if (!kb) {
            if (this.auto_reconstruction)
                kb = this.get_keyboard(document);
            else
                return;
        }
        kb.classList.toggle('emojikb-hidden');
    }

    add_emojis(emojis) {
        for (const e of emojis) {
            if (!(e.url && e.name)) continue;
            this.custom_emojis.push({
                url: e.url,
                name: e.name
            });
        }
    }

    async wait_for_ready() {
        let tests = 0; // max 15s waiting
        const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))
        while (tests < 30 && this.emojis.get("People").length === 0) {
            await sleep(500);
            tests++;
        }
        if (tests == 30) {
            console.error("Unable to instantiate emojis")
        }
    }


    // ----- PRIVATE PART ----- you should not need to call that ----- //

    get_keyboard(document) {
        let kb = document.getElementById("emojikb-maindiv");
        if (!kb)
            kb = this.create_keyboard(document);
        return kb
    }

    click_on_emoji(kb, event) {
        if (!event.shiftKey) kb.toggle_window();
        const data = Object.assign({}, event.target.dataset)
        kb.callback(data, !event.shiftKey);
    }

    hover_on_emoji(kb, event) {
        const document = event.target.ownerDocument;
        const name = event.target.dataset.name;
        const url = event.target.src;
        document.getElementById("emojikb-info-name").innerText = name;
        document.getElementById("emojikb-info-icon").src = url;
        document.getElementById("emojikb-textinput").placeholder = name;
        event.target.classList.add("selected");
    }

    hover_out_emoji(kb, event) {
        const document = event.target.ownerDocument;
        document.getElementById("emojikb-textinput").placeholder = kb.default_placeholder;
        event.target.classList.remove("selected");
    }

    click_on_category(kb, event, stay) {
        let target;
        if (event.target) {
            target = event.target.nodeName == "path" ? event.target.parentNode : event.target;
        } else target = event;
        $('#emojikb-leftlist>svg.selected').removeClass('selected');
        target.classList.add("selected");
        if (!stay) { // scroll to the corresponding category
            const categ = target.dataset.emojikb_categ;
            const targets = target.ownerDocument.querySelectorAll('div.emojikb-categname[data-emojikb_categ="' + categ + '"]');
            if (!targets[0]) return;
            targets[0].parentNode.scrollIntoView(true, {behavior: "instant"}); // let's not trigger hundreds of lazy loading
            targets[0].parentNode.parentNode.scrollTop++; // make sure the observator is triggered
        }
    }

    on_typing(event) {
        if (event.target.value === "") {
            event.target.ownerDocument.querySelectorAll('img.emojikb-emoji').forEach(e => {
                e.classList.toggle('emojikb-hidden', false);
            })
            event.target.ownerDocument.querySelectorAll('div.emojikb-categ').forEach(e => {
                e.classList.toggle('emojikb-hidden', false);
            })
            return;
        }
        if (!this.fuse) this.init_fuse();
        const result = Array.from(this.fuse.search(event.target.value), e => e.item.name);
        let hiddens = new Map(Array.from(this.categories, v => [v, 0]));
        event.target.ownerDocument.querySelectorAll('img.emojikb-emoji').forEach(e => {
            e.classList.toggle('emojikb-hidden', !result.includes(e.dataset.name));
            if (!result.includes(e.dataset.name)) {
                hiddens.set(e.dataset.category, hiddens.get(e.dataset.category) + 1);
            }
        })
        event.target.ownerDocument.querySelectorAll('div.emojikb-categ').forEach(e => {
            const hidden_nbr = hiddens.get(e.firstChild.dataset['emojikb_categ']);
            e.classList.toggle('emojikb-hidden', e.childElementCount <= hidden_nbr + 1);
        })
    }

    init_fuse() {
        // https://fusejs.io/
        let flattened = [];
        for (const list of this.emojis.values()) {
            flattened = flattened.concat(list);
        }
        this.fuseIndex = Fuse.createIndex(['name', 'unicode'], flattened);
        this.fuse = new Fuse(flattened, {
            keys: [{
                name: 'name',
                weight: 0.7
            }, {
                name: 'unicode',
                weight: 0.3
            }],
            minMatchCharLength: 2,
            threshold: 0.35,
            distance: 15
        }, this.fuseIndex);
    }

    init_base_emojis() {
        // https://gist.github.com/oliveratgithub/0bf11a9aff0d6da7b46f1490f86a71eb
        fetch("https://gist.githubusercontent.com/oliveratgithub/0bf11a9aff0d6da7b46f1490f86a71eb/raw/d8e4b78cfe66862cf3809443c1dba017f37b61db/emojis.json").then(async response => {
            var contentType = response.headers.get("content-type");
            if (contentType && (contentType.includes("application/json") || contentType.includes("text/plain"))) {
                const json = await response.json();
                json.emojis.forEach(emoji => {
                    if (emoji.shortname.includes('_skin_tone') || emoji.unicode.includes(':'))
                        // invalid emojis
                        return;
                    const categ = this.find_right_category(emoji.category);
                    if (!categ)
                        return;
                    this.emojis.get(categ).push({
                        emoji: emoji.emoji,
                        url: "https://twemoji.maxcdn.com/v/13.0.1/72x72/" + emoji.unicode.replace(/ /g, '-').toLowerCase() + ".png",
                        name: emoji.shortname,
                        unicode: emoji.unicode
                    });
                });
            } else {
                console.error("Oops, can't get the usual emojis list! (invalid format)");
            }
        })
    }

    find_right_category(subcategory) {
        if (!subcategory) return;
        try {
            let sub_name = subcategory.match(/[^(]+/)[0].trim();
            for (const [k, v] of categories) {
                if (v.includes(sub_name))
                    return k;
            }
        } catch (err) {
            console.error(err);
        }
        console.warn("Missing emoji category:", subcategory)
    }

    create_keyboard(document) {
        const dom_parser = new DOMParser();
        const parse_svg = (x) => dom_parser.parseFromString(x, "text/xml").firstChild;
        let main_div = document.createElement("div");
        main_div.id = "emojikb-maindiv";
        if (screen.width > 570)
            main_div.style.width = '33.5%';
        else if (screen.width <= 570)
            main_div.style.width = '100%'
        if (this.resizable) {
            main_div.classList.add('resizable');
            main_div.dataset.m_pos = 0;
            const f = (e) => {
                this.resize(e, main_div)
            };
            main_div.addEventListener("mousedown", (e) => {
                if (e.offsetX < 4) {
                    main_div.dataset.m_pos = e.x;
                    document.addEventListener("mousemove", f, false);
                }
            }, false);
            document.addEventListener("mouseup", () => {
                document.removeEventListener("mousemove", f, false);
            }, false);
        }
        // search div
        let search_div = document.createElement("div");
        search_div.id = "emojikb-searchdiv";
        // let s_div = document.createElement("div");
        let s_area = document.createElement("input");
        s_area.id = "emojikb-textinput";
        s_area.placeholder = this.default_placeholder;
        s_area.addEventListener('input', (e) => this.on_typing(e))
        search_div.appendChild(s_area);
        search_div.appendChild(parse_svg(SVG_HTML.search));
        // under the search div
        let div2 = document.createElement("div");
        div2.id = "emojikb-div2";
        // categories list
        let list_div = document.createElement("div");
        list_div.id = "emojikb-leftlist";
        let div3 = document.createElement("div");
        div3.id = "emojikb-div3";
        // emojis list
        let emojis_div = document.createElement("div");
        emojis_div.id = "emojikb-show";
        // filling lists
        let first_emoji;
        for (const v of [
            [SVG_HTML.custom, 'Custom'],
            [SVG_HTML.head, 'People'],
            [SVG_HTML.leaf, 'Nature'],
            [SVG_HTML.food, 'Food'],
            [SVG_HTML.game, 'Activities'],
            [SVG_HTML.submarine, 'Travel'],
            [SVG_HTML.tea, 'Objects'],
            [SVG_HTML.heart, 'Symbols'],
            [SVG_HTML.flag, 'Flags']
        ]) {
            if (this.emojis.get(v[1])?.length === 0) {
                continue
            }
            ;
            let elem = parse_svg(v[0]);
            elem.dataset['emojikb_categ'] = v[1];
            elem.addEventListener('click', e => this.click_on_category(this, e));
            list_div.appendChild(elem);
            // emojis grid
            let categ_div = document.createElement("div");
            categ_div.className = "emojikb-categ";
            let categ_name = document.createElement("div");
            categ_name.className = "emojikb-categname";
            categ_name.dataset['emojikb_categ'] = v[1];
            if (this.stickyObserver) {
                this.stickyObserver.observe(categ_name);
            }
            let categ_span = document.createElement("span");
            categ_span.innerText = v[1];
            categ_name.appendChild(parse_svg(v[0]));
            categ_name.appendChild(categ_span);
            categ_div.appendChild(categ_name);
            for (const emoji of this.emojis.get(v[1]).sort((a, b) => a.unicode.localeCompare(b.unicode))) {
                let img = document.createElement("img");
                img.dataset.name = emoji.name;
                img.dataset.unicode = emoji.unicode;
                img.dataset.emoji = emoji.emoji;
                img.dataset.category = v[1];
                img.className = "emojikb-emoji";
                first_emoji = first_emoji || emoji;
                if (this.lazyImageObserver) {
                    this.lazyImageObserver.observe(img);
                    img.dataset.src = emoji.url;
                    img.classList.add('lazy');
                } else {
                    img.src = emoji.url;
                }
                img.addEventListener('error', err => {
                    // console.info(err.target.dataset);
                    const data = err.target.dataset;
                    const index = this.emojis.get(data.category).findIndex(e => e.name == data.name);
                    if (index) this.emojis.get(data.category).splice(index, 1);
                    err.target.remove();
                    this.init_fuse(); // refresh search index
                });
                img.addEventListener('click', e => this.click_on_emoji(this, e));
                img.addEventListener('mouseenter', e => this.hover_on_emoji(this, e));
                img.addEventListener('mouseleave', e => this.hover_out_emoji(this, e));
                categ_div.appendChild(img);
            }
            emojis_div.appendChild(categ_div);
        }
        // emoji info
        let info_div = document.createElement("div");
        info_div.id = "emojikb-info";
        let info_icon = document.createElement("img");
        info_icon.id = "emojikb-info-icon";
        info_icon.src = first_emoji.url;
        let info_name = document.createElement("div");
        info_name.id = "emojikb-info-name";
        info_name.innerText = first_emoji.name;
        info_div.appendChild(info_icon);
        info_div.appendChild(info_name);
        // we add everything together
        div3.appendChild(emojis_div);
        div3.appendChild(info_div);
        div2.appendChild(list_div);
        div2.appendChild(div3);
        main_div.appendChild(search_div);
        main_div.appendChild(div2);
        document.documentElement.appendChild(main_div);
    }

    // ----- resizes part ----- //

    resize(e, panel) {
        const dx = panel.dataset.m_pos - e.x;
        panel.dataset.m_pos = e.x;
        panel.style.width = (parseInt(getComputedStyle(panel, '').width) + dx) + "px";
    }
}

SVG_HTML = {
    search: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>',
    head: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.477 2 12C2 17.522 6.477 22 12 22C17.523 22 22 17.522 22 12C22 6.477 17.522 2 12 2ZM16.293 6.293L17.707 7.706L16.414 9L17.707 10.293L16.293 11.706L13.586 9L16.293 6.293ZM6.293 7.707L7.707 6.294L10.414 9L7.707 11.707L6.293 10.294L7.586 9L6.293 7.707ZM12 19C9.609 19 7.412 17.868 6 16.043L7.559 14.486C8.555 15.92 10.196 16.831 12 16.831C13.809 16.831 15.447 15.92 16.443 14.481L18 16.04C16.59 17.867 14.396 19 12 19Z"></path></svg>',
    leaf: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M6.814 8.982C4.539 11.674 4.656 15.591 6.931 18.153L4.034 21.579L5.561 22.87L8.463 19.437C9.569 20.127 10.846 20.513 12.161 20.513C14.231 20.513 16.183 19.607 17.516 18.027C20.069 15.01 20.771 6.945 21 3C17.765 3.876 9.032 6.356 6.814 8.982V8.982ZM8.935 17.331C6.826 15.548 6.56 12.382 8.342 10.272C9.592 8.793 14.904 6.845 18.764 5.698L8.935 17.331V17.331Z"></path></svg>',
    food: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M11 18H13V22H11V18Z"></path><path d="M12 2C8.822 2 7 4.187 7 8V16C7 16.552 7.447 17 8 17H16C16.553 17 17 16.552 17 16V8C17 4.187 15.178 2 12 2ZM11 14.001H10V5.001H11V14.001ZM14 14.001H13V5.001H14V14.001Z"></path></svg>',
    game: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5.66487 5H18.3351C19.9078 5 21.2136 6.21463 21.3272 7.78329L21.9931 16.9774C22.0684 18.0165 21.287 18.9198 20.248 18.9951C20.2026 18.9984 20.1572 19 20.1117 19C18.919 19 17.8785 18.1904 17.5855 17.0342L17.0698 15H6.93015L6.41449 17.0342C6.12142 18.1904 5.08094 19 3.88826 19C2.84645 19 2.00189 18.1554 2.00189 17.1136C2.00189 17.0682 2.00354 17.0227 2.00682 16.9774L2.67271 7.78329C2.78632 6.21463 4.0921 5 5.66487 5ZM14.5 10C15.3284 10 16 9.32843 16 8.5C16 7.67157 15.3284 7 14.5 7C13.6716 7 13 7.67157 13 8.5C13 9.32843 13.6716 10 14.5 10ZM18.5 13C19.3284 13 20 12.3284 20 11.5C20 10.6716 19.3284 10 18.5 10C17.6716 10 17 10.6716 17 11.5C17 12.3284 17.6716 13 18.5 13ZM6.00001 9H4.00001V11H6.00001V13H8.00001V11H10V9H8.00001V7H6.00001V9Z"></path></svg>',
    submarine: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M22 17H19.725C19.892 16.529 20 16.029 20 15.5C20 13.015 17.985 11 15.5 11H13.5L12.276 8.553C12.107 8.214 11.761 8 11.382 8H7C6.448 8 6 8.447 6 9V11.051C3.753 11.302 2 13.186 2 15.5C2 17.986 4.015 20 6.5 20H15.5C16.563 20 17.527 19.616 18.297 19H22V17ZM6.5 16.75C5.81 16.75 5.25 16.19 5.25 15.5C5.25 14.81 5.81 14.25 6.5 14.25C7.19 14.25 7.75 14.81 7.75 15.5C7.75 16.19 7.19 16.75 6.5 16.75ZM11.5 16.75C10.81 16.75 10.25 16.19 10.25 15.5C10.25 14.81 10.81 14.25 11.5 14.25C12.19 14.25 12.75 14.81 12.75 15.5C12.75 16.19 12.19 16.75 11.5 16.75ZM16.5 16.75C15.81 16.75 15.25 16.19 15.25 15.5C15.25 14.81 15.81 14.25 16.5 14.25C17.19 14.25 17.75 14.81 17.75 15.5C17.75 16.19 17.19 16.75 16.5 16.75Z"></path><path d="M8 7H10C10 5.346 8.654 4 7 4H6V6H7C7.551 6 8 6.449 8 7Z"></path></svg>',
    tea: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18 5.999H17V4.999C17 4.448 16.553 3.999 16 3.999H4C3.447 3.999 3 4.448 3 4.999V12.999C3 14.488 3.47 15.865 4.265 16.999H15.722C16.335 16.122 16.761 15.105 16.92 13.999H18C20.205 13.999 22 12.205 22 9.999C22 7.794 20.205 5.999 18 5.999V5.999ZM18 12H17V8H18C19.104 8 20 8.897 20 10C20 11.102 19.104 12 18 12Z"></path><path d="M2 18H18V20H2V18Z"></path></svg>',
    heart: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M16 4.001C14.406 4.001 12.93 4.838 12 6.081C11.07 4.838 9.594 4.001 8 4.001C5.243 4.001 3 6.244 3 9.001C3 14.492 11.124 19.633 11.471 19.849C11.633 19.95 11.817 20.001 12 20.001C12.183 20.001 12.367 19.95 12.529 19.849C12.876 19.633 21 14.492 21 9.001C21 6.244 18.757 4.001 16 4.001V4.001Z"></path></svg>',
    flag: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 6.002H14V3.002C14 2.45 13.553 2.002 13 2.002H4C3.447 2.002 3 2.45 3 3.002V22.002H5V14.002H10.586L8.293 16.295C8.007 16.581 7.922 17.011 8.076 17.385C8.23 17.759 8.596 18.002 9 18.002H20C20.553 18.002 21 17.554 21 17.002V7.002C21 6.45 20.553 6.002 20 6.002Z"></path></svg>',
    custom: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M4 8h4V4H4v4zm6 12h4v-4h-4v4zm-6 0h4v-4H4v4zm0-6h4v-4H4v4zm6 0h4v-4h-4v4zm6-10v4h4V4h-4zm-6 4h4V4h-4v4zm6 6h4v-4h-4v4zm0 6h4v-4h-4v4z"/></svg>'
}