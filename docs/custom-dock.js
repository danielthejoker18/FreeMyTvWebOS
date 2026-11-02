/* Minimal dock presentation; the existing webOS app launcher stays intact. */
(function () {
    'use strict';
    var defaults = ['netflix', 'spotify-beehive', 'auto-apple-tv', 'auto-switch'];
    var slots = defaults.slice();
    var overlay = document.getElementById('allAppsDrawer');
    var drawerGrid = document.getElementById('allAppsGrid');
    var drawerOpen = false, cards = [], selected = 0;
    var oldRender = window.renderAppsShelf;
    try {
        var saved = JSON.parse(localStorage.getItem('fmtv_dock_slots') || 'null');
        if (Array.isArray(saved) && saved.length === 4 &&
            saved.every(function (s) { return typeof s === 'string'; })) slots = saved;
    } catch (e) {}

    function getApp(id) {
        for (var i = 0; i < state.catalog.length; i++) {
            if (state.catalog[i].id === id) return state.catalog[i];
        }
        return null;
    }
    function resolve(token) {
        var i, app;
        if (token === 'auto-apple-tv') {
            for (i = 0; i < state.catalog.length; i++) {
                app = state.catalog[i];
                if (/^apple tv/i.test(app.title || '') || /appletv/i.test(app.id || '')) return app;
            }
            return null;
        }
        if (token === 'auto-switch') {
            for (i = 0; i < state.catalog.length; i++) {
                app = state.catalog[i];
                if (isHDMI(app) && state.hdmiDevices[app.id] === 'switch') return app;
            }
            return null;
        }
        return getApp(token);
    }
    function getDockApps() {
        var found = [], used = {};
        slots.forEach(function (token) {
            var app = resolve(token);
            if (app && !used[app.id]) { found.push(app); used[app.id] = true; }
        });
        state.favorites.concat(state.catalog.map(function (app) { return app.id; }))
            .forEach(function (id) {
                var app = getApp(id);
                if (found.length < 4 && app && !used[id]) {
                    found.push(app);
                    used[id] = true;
                }
            });
        return found.slice(0, 4);
    }
    function paint(app, button) {
        var icon = document.createElement('div');
        var device = devicePreset(app, state.hdmiDevices);
        icon.className = 'app-icon';
        icon.style.background = 'rgba(23,28,41,.54)';
        if (isHDMI(app)) {
            icon.style.background = 'rgba(100,29,48,.42)';
            if (device.logo) {
                var fb = document.createElement('span');
                fb.className = 'app-art-fallback';
                fb.textContent = device.title || app.title;
                icon.appendChild(fb);
                addTileImage(icon, 'assets/brands/' + device.logo + '.svg', true);
            } else icon.innerHTML = deviceArtwork(device.shape);
        } else {
            if (app.id === 'netflix') icon.style.background = 'rgba(23,8,16,.66)';
            else if (app.id === 'spotify-beehive') icon.style.background = 'rgba(11,39,26,.66)';
            var fb2 = document.createElement('span');
            fb2.className = 'app-art-fallback';
            fb2.textContent = app.title;
            icon.appendChild(fb2);
            var logo = APP_LOGOS[app.id];
            if (logo || app.iconUrl)
                addTileImage(icon, logo ? 'assets/brands/' + logo + '.svg' : app.iconUrl, !!logo);
        }
        button.appendChild(icon);
    }
    function tile(app, dockTile) {
        var btn = document.createElement('button');
        var title = devicePreset(app, state.hdmiDevices).title || app.title;
        btn.className = dockTile ? 'app-tile nav-item' : 'all-app-card';
        btn.dataset.id = app.id;
        btn.setAttribute('aria-label', title);
        if (dockTile) {
            btn.dataset.title = title;
            btn.dataset.tag = app.tag;
            btn.dataset.desc = app.desc;
            btn.dataset.color = app.color;
        }
        paint(app, btn);
        if (!dockTile) {
            var caption = document.createElement('span');
            caption.className = 'all-app-card-title';
            caption.textContent = title;
            btn.appendChild(caption);
        }
        btn.addEventListener('mouseenter', function () {
            if (dockTile) setMainFocus(btn);
            else focusCard(btn);
        });
        btn.addEventListener('click', function () {
            if (!dockTile) closeDrawer();
            launchApp(app.id);
        });
        return btn;
    }
    function dockRender() {
        if (shelfEdit) { oldRender(); return; } // preserve original 12-app reorder UI
        var grid = document.getElementById('appsGrid');
        grid.innerHTML = '';
        getDockApps().forEach(function (app) { grid.appendChild(tile(app, true)); });
        var more = document.createElement('button');
        more.className = 'app-tile more-tile nav-item';
        more.id = 'moreAppsBtn';
        more.dataset.id = '__more__';
        more.setAttribute('aria-label', 'All apps and inputs');
        var dots = document.createElement('span');
        dots.className = 'more-dots';
        dots.setAttribute('aria-hidden', 'true');
        dots.textContent = '•••';
        more.appendChild(dots);
        more.addEventListener('mouseenter', function () { setMainFocus(more); });
        more.addEventListener('click', openDrawer);
        grid.appendChild(more);
        refreshMainNavList();
    }
    function focusCard(btn) {
        if (!btn) return;
        cards.forEach(function (x) { x.classList.remove('focused'); });
        btn.classList.add('focused');
        btn.focus();
        selected = cards.indexOf(btn);
        var box = btn.getBoundingClientRect();
        var bounds = drawerGrid.getBoundingClientRect();
        if (box.bottom > bounds.bottom - 8) drawerGrid.scrollTop += box.bottom - bounds.bottom + 14;
        else if (box.top < bounds.top + 8) drawerGrid.scrollTop -= bounds.top - box.top + 14;
    }
    function openDrawer() {
        if (shelfEdit) return;
        drawerOpen = true;
        overlay.classList.add('active');
        drawerGrid.innerHTML = '';
        cards = [];
        var shown = {};
        getDockApps().forEach(function (app) { shown[app.id] = true; });
        state.favorites.concat(state.catalog.map(function (app) { return app.id; }))
            .forEach(function (id) {
                if (shown[id]) return;
                shown[id] = true;
                var app = getApp(id);
                if (!app) return;
                var btn = tile(app, false);
                drawerGrid.appendChild(btn);
                cards.push(btn);
            });
        if (cards.length) focusCard(cards[0]);
        else document.getElementById('closeAllAppsBtn').focus();
    }
    function closeDrawer() {
        drawerOpen = false;
        overlay.classList.remove('active');
        var more = document.getElementById('moreAppsBtn');
        if (more) setMainFocus(more);
    }
    function moveCard(key) {
        if (!cards.length) return;
        var cols = window.innerWidth <= 1000 ? 3 : 4;
        var n = selected + (key === 'ArrowDown' ? cols :
            key === 'ArrowUp' ? -cols : key === 'ArrowRight' ? 1 : -1);
        if (n < 0 || n >= cards.length) return;
        if ((key === 'ArrowLeft' || key === 'ArrowRight') &&
            Math.floor(n / cols) !== Math.floor(selected / cols)) return;
        focusCard(cards[n]);
    }
    document.addEventListener('keydown', function (e) {
        if (!drawerOpen) return;
        if (e.keyCode === 461 || e.key === 'Escape' || e.key === 'GoBack') closeDrawer();
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight' ||
                 e.key === 'ArrowUp' || e.key === 'ArrowDown') moveCard(e.key);
        else if (e.key === 'Enter') {
            if (cards.length) cards[selected].click();
            else closeDrawer();
        } else return;
        e.preventDefault();
        e.stopImmediatePropagation();
    }, true);
    document.getElementById('closeAllAppsBtn').addEventListener('click', closeDrawer);

    function populateDockSettings() {
        for (var i = 0; i < 4; i++) {
            var picker = document.getElementById('cfgDock' + (i + 1));
            picker.innerHTML = '';
            if (i === 2 || i === 3) {
                var special = document.createElement('option');
                special.value = i === 2 ? 'auto-apple-tv' : 'auto-switch';
                special.textContent = i === 2 ? 'Apple TV (auto)' : 'Nintendo Switch (configured HDMI)';
                picker.appendChild(special);
            }
            state.catalog.forEach(function (app) {
                var option = document.createElement('option');
                option.value = app.id;
                option.textContent = devicePreset(app, state.hdmiDevices).title || app.title;
                picker.appendChild(option);
            });
            picker.value = slots[i];
            if (picker.selectedIndex < 0) picker.selectedIndex = 0;
        }
    }
    document.getElementById('customizeBtn').addEventListener('click', populateDockSettings);
    document.getElementById('resetDefaultBtn').addEventListener('click', function () {
        slots = defaults.slice();
        populateDockSettings();
    });
    document.getElementById('saveModalBtn').addEventListener('click', function () {
        slots = [];
        for (var i = 0; i < 4; i++)
            slots.push(document.getElementById('cfgDock' + (i + 1)).value);
        try { localStorage.setItem('fmtv_dock_slots', JSON.stringify(slots)); } catch (e) {}
        dockRender();
    });
    window.renderAppsShelf = dockRender;
    dockRender();
})();
