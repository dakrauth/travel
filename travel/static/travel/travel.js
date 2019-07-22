//------------------------------------------------------------------------------
// Sample entity object
//------------------------------------------------------------------------------
// entity = {
//     "flag_svg": "img/wh-32.png",
//     "code": "3",
//     "name": "Aachen Cathedral",
//     "locality": "State of North Rhine-Westphalia (Nordrhein-Westfalen)",
//     "country_flag_svg": "img/flags/co/de/de-32.png",
//     "country_code": "DE",
//     "country_name": "Germany",
//     "type_abbr": "wh",
//     "id": 11942
// }
//}
//------------------------------------------------------------------------------

;const Travelogue = (function(root) {
    const timeit = (fn, ...args) => {
        const start = new Date();
        const result = fn.call(undefined, ...args);
        const end = new Date();
        const delta = end - start
        console.log(`timeit: ${start.toJSON()} => ${end.toJSON()} = ${delta}`);
        return result;
    };

    const fetch = function(url, handler) {
        const success_wrapper = function() { handler(JSON.parse(xhr.responseText)); };
        const xhr = new XMLHttpRequest();
        xhr.addEventListener('load', success_wrapper);
        xhr.open("GET", url);
        xhr.send();
    };

    const TYPE_MAPPING = {
        'cn': 'Continents', 'co': 'Countries', 'wh': 'World Heritage sites',
        'st': 'States',     'ap': 'Airports',  'np': 'National Parks',
        'lm': 'Landmarks',  'ct': 'Cities'
    };

    const sorters = {
        type: (a, b) => (b.entity.type_abbr > a.entity.type_abbr) ? 1: -1,
        name: (a, b) => (b.entity.name > a.name) ? 1 : -1,
        recent_visit: (a, b) => b.arrival.valueOf() - a.arrival.valueOf(),
        first_visit: (a, b) => {
            const aLogs = a.entity.logs;
            const bLogs = b.entity.logs;
            return (
                bLogs[bLogs.length - 1].arrival.valueOf()
              - aLogs[aLogs.length - 1].arrival.valueOf()
            );
        },
        num_visits: (a, b) => b.entity.logs.length - a.entity.logs.length,
        rating: (a, b) => a.rating - b.rating
    };

    const DATE_STRING  = 'MMM Do YYYY';
    const TIME_STRING  = 'ddd h:ssa';
    const DATE_FORMAT  = 'YYYY-MM-DD';

    const stars = rating => '★★★★★'.substr(rating - 1);

    const DOM = {
        get(q, ctx) {
            return document.querySelector(q, ctx)
        },
        create(tag, ...args) {
            const el = document.createElement(tag);
            for(const arg of args) {
                if(Array.isArray(arg)) {
                    arg.forEach(child => el.appendChild(child));
                }
                else if(typeof arg === 'string') {
                    el.textContent = arg;
                }
                else {
                    Object.keys(arg).forEach(key => el.setAttribute(key, arg[key]));
                }
            };
            return el;
        }
    };

    const dateTags = dtw => [
        DOM.create('div', dtw.format(DATE_STRING)),
        DOM.create('div', dtw.format(TIME_STRING))
    ];

    const createLogRow = log => {
        let extras = [];
        const e = log.entity;
        const nameTd = DOM.create('td');
        const flagTd = DOM.create('td');
        const firstArrival = e.logs[e.logs.length-1].arrival;
        const attrs = {
            'data-id': e.id,
            'data-name': e.name,
            'data-arrival': log.arrival.valueOf(),
            'data-first': firstArrival.valueOf(),
            'data-count': e.logs.length,
            'data-rating': log.rating,
            'class': e.type_abbr + ' co-' + (
                e.country_code ?
                e.country_code :
                (e.type_abbr == 'co' ? e.code : '')
            )
        };

        nameTd.appendChild(DOM.create('a', e.name, {'href': e.url()}));
        if(e.flag_svg) {
            flagTd.appendChild(DOM.create('img', {'src': e.flag_svg, 'class': 'flag flag-sm'}));
        }

        e.locality && extras.push(e.locality);
        e.country_name && extras.push(e.country_name);
        if(extras.length) {
            nameTd.appendChild(DOM.create('span', extras.join(', ')));
        }

        if(e.country_flag_emoji) {
            nameTd.appendChild(DOM.create('span', e.country_flag_emoji));
        }
        else if(e.country_flag_svg) {
            nameTd.appendChild(DOM.create('img', {
                'src': e.country_flag_svg,
                'class': 'flag flag-xs'
            }));
        }

        return DOM.create('tr', attrs, [
            flagTd,
            DOM.create('td', TYPE_MAPPING[e.type_abbr]),
            nameTd,
            DOM.create('td', {'class': 'when'}, dateTags(log.arrival)),
            DOM.create('td', {'class': 'when'}, dateTags(firstArrival)),
            DOM.create('td', e.logs.length.toString()),
            DOM.create('td', stars(log.rating))
        ]);
    };

    const getOrdering = el => {
        const ordering = {'column': el.dataset.column, 'order': el.dataset.order};
        const current = el.parentElement.querySelector('.current');
        if(el === current) {
            ordering.order = (ordering.order === 'desc') ? 'asc' : 'desc';
            el.dataset.order = ordering.order;
        }
        else {
            current.className = '';
            el.className = 'current';
        }
        return ordering;
    };

    const showSummary = summary => {
        const el = DOM.get('#summary');
        while(el.lastChild) {
          el.removeChild(el.lastChild);
        }

        el.appendChild(DOM.create('strong', 'Summary: '));
        for(const key of Object.keys(summary)) {
            const items = Object.keys(summary[key]).length;
            if(items) {
                el.appendChild(DOM.create(
                    'span',
                    {'class': 'label label-info'},
                    TYPE_MAPPING[key] + ': ' + items
                ));
            }
        }
    };

    class Summary {
        constructor() {
            for(const key of Object.keys(TYPE_MAPPING)) {
                this[key] = {};
            }
        }
        add(e) {
            const kind = this[e.type_abbr];
            kind[e.id] = 1 + (kind[e.id] || 0);
        }
    }

    class LogEntry{
        constructor(e) {
            Object.assign(this, e);
            this.logs = [];
        }
        url() {
            let bit = this.code;
            if(this.type_abbr == 'wh' || this.type_abbr == 'st') {
                bit = this.country_code + '-' + bit;
            }
            return '/i/' + this.type_abbr + '/' + bit + '/';
        }
    }

    class TravelLogs {
        constructor(logs, summary) {
            this.logs = logs;
            this.summary = summary;
        }
        sortLogs(column, order) {
            console.log('ordering', column, order);
            this.logs.sort(sorters[column]);
            if(order === 'desc') {
                this.logs.reverse()
            }
        }
        filter(bits) {
            console.log('filter bits', bits);
            this.summary = new Summary();
            for(const log of this.logs) {
                const e = log.entity;
                let good = true;
                if(bits.type) {
                    good = (e.type_abbr === bits.type);
                }

                if(good && bits.co) {
                    good = (
                        e.country_code === bits.co ||
                        (e.type_abbr === 'co' && e.code === bits.co)
                    );
                }

                if(good && bits.limit) {
                    if(e.logs.length === 1) {
                        good = true;
                    }
                    else if(bits.limit === 'recent') {
                        good = e.logs[0].id === log.id;
                    }
                    else {
                        good = e.logs[e.logs.length - 1].id == log.id;
                    }
                }

                if(good && bits.timeframe && bits.date) {
                    switch(bits.timeframe) {
                        case '+':
                            good = log.arrival.isAfter(bits.date);
                            break;
                        case '-':
                            good = log.arrival.isBefore(bits.date);
                            break;
                        case '=':
                            good = (log.arrival.year() === bits.date);
                            break;
                        default:
                            good = false;
                    }
                }

                if(good) {
                    this.summary.add(e);
                }

                log.isActive = good;
            }

            return this;
        }
    }

    const showLogs = travelLogs => {
        const start = new Date();
        const count = travelLogs.logs.length;
        let parent = DOM.get('#history');
        let el = parent.querySelector('tbody');

        DOM.get('#id_count').textContent = (count + ' entr' + (count > 1 ? 'ies' : 'y'));
        el.parentNode.removeChild(el);
        el = DOM.create('tbody');
        for(const log of travelLogs.logs) {
            if(log.isActive) {
                el.appendChild(createLogRow(log));
            }
        }
        parent.appendChild(el);
        showSummary(travelLogs.summary);
        console.log('delta', new Date() - start);
    };

    const initOrderingByColumns = controller => {
        for(const e of document.querySelectorAll('#history thead th[data-column]')) {
            e.addEventListener('click', evt => {
                const ordering = getOrdering(e);
                if(ordering.order === 'asc') {
                    HashBits.fromFilters().update();
                }
                controller.sortLogs(ordering.column, ordering.order);
            }, false)
        };
    };

    const createCountryOptions = countries => {
        const cos = DOM.get('#id_co');
        for(const key of Object.keys(countries).sort()) {
            cos.appendChild(DOM.create('option', countries[key], {'value': key}));
        }
    };

    const createYearsOption = keys => {
        const sel = DOM.create('select', {
            'class': 'filter_ctrl form-control input-sm',
            'id': 'id_years'
        });

        sel.style.display = 'none';
        for(const yr of keys.sort((a, b) => { return b - a; })) {
            sel.appendChild(DOM.create('option', yr, {'value': yr}));
        }
        DOM.get('#id_date').parentElement.appendChild(sel);
    };

    const initProfileFilter = (controller, conf) => {
        const onFilterChange = () => {
            const bits = HashBits.fromFilters();
            console.log(bits);
            bits.update();
            controller.filterLogs(bits);
        };
        const onHashChange = () => {
            const bits = HashBits.fromHash();
            setFilterFields(bits);
            controller.filterLogs(bits);
        };
        const dateEl = DOM.get('#id_date');
        new Pikaday({
            field: dateEl,
            format: DATE_FORMAT,
            minDate: new Date(1920,1,1),
            yearRange: [1920, (new Date()).getFullYear()],
            onSelect: dt => { console.log(dt, this); }
        });

        window.addEventListener('hashchange', onHashChange, false);
        DOM.get('#id_timeframe').addEventListener('change', () => {
            if(this.value === '=') {
                DOM.get('#id_years').style.display = 'inline-block';
                dateEl.style.display = 'none';
            }
            else {
                dateEl.style.display = 'inline-block';
                DOM.get('#id_years').style.display = 'none';
            }
        }, false);

        dateEl.addEventListener('input', onFilterChange, false);
        dateEl.addEventListener('propertychange', onFilterChange, false);
        for(const e of document.querySelectorAll('.filter_ctrl')) {
            e.addEventListener('change', onFilterChange, false);
        }

        onHashChange();
    };

    const controller = {
        initialize(entities, logs, conf) {
            const countries = {};
            const yearSet = {};
            const summary = new Summary();
            const entityDict = {};
            this.logEntries = [];
            for(const entity of entities) {
                const e = new LogEntry(entity);
                this.logEntries.push(e);
                if(e.country_code) {
                    countries[e.country_code] = e.country_name;
                }
                entityDict[e.id] = e;
            }
            for(const log of logs) {
                log.entity = entityDict[log.entity];
                if(!log.entity) { console.log(log); }

                log.entity.logs.push(log);
                log.arrival = moment(log.arrival);
                log.isActive = true;
                yearSet[log.arrival.year()] = true;
                summary.add(log.entity);
            }

            this.logs = new TravelLogs(logs, summary);
            console.log(summary);
            createCountryOptions(countries);
            initOrderingByColumns(this);
            createYearsOption(Object.keys(yearSet));
            initProfileFilter(this, conf);
        },
        filterLogs(bits) {
            this.logs.filter(bits);
            showLogs(this.logs);
        },
        sortLogs(column, order) {
            this.logs.sortLogs(column, order);
            showLogs(this.logs);
        }
    };

    class HashBits {
        static fromHash(hash) {
            const bits = new HashBits();
            hash = hash || window.location.hash;
            if(hash && hash[0] == '#') {
                hash = hash.substr(1);
            }

            if(hash) {
                for(const bit of hash.split('/')) {
                    const kvp = bit.split(':');
                    bits[kvp[0]] = (kvp.length === 2) ? kvp[1] : true;
                }

                if(bits.date) {
                    bits.timeframe = bits.date[0];
                    bits.date = (bits.timeframe === '=')
                              ? parseInt(bits.date.substr(1))
                              : moment(bits.date.substr(1));
                }
            }
            return bits;
        }
        static fromFilters() {
            const bits = new HashBits();
            const dt = DOM.get('#id_date').value;
            const el = document.querySelector('#history thead .current');
            bits.type = DOM.get('#id_filter').value;
            bits.co   = DOM.get('#id_co').value;
            bits.timeframe = DOM.get('#id_timeframe').value;
            bits.limit = DOM.get('#id_limit').value;

            if(bits.timeframe === '=') {
                bits.date = parseInt(DOM.get('#id_years').value);
            }
            else if(bits.timeframe) {
                bits.date = dt ? moment(dt) : null;
            }
            if(el && el.dataset.order == 'asc') {
                bits.asc = el.dataset.column;
            }
            return bits;
        }
        toString() {
            let a = [];
            for(const bit of ['type', 'co', 'asc', 'limit']) {
                if(this[bit]) {
                    a.push(bit + ':' + this[bit]);
                }
            }
            if(this.timeframe === '-' || this.timeframe === '+') {
                if(this.date) {
                    a.push('date:' + this.timeframe + this.date.format(DATE_FORMAT));
                }
            }
            else if(this.timeframe === '=') {
                if(this.date) {
                    a.push('date:' + this.timeframe + this.date);
                }
            }
            return a.length ? '#' + a.join('/') : './';
        }
        update() {
            window.history.pushState({}, '', this.toString());
        }
    }

    const setFilterFields = bits => {
        const yearsEl = DOM.get('#id_years');
        const dateEl = DOM.get('#id_date');
        DOM.get('#id_filter').value = bits.type || '';
        DOM.get('#id_timeframe').value = bits.timeframe || '';
        DOM.get('#id_co').value = bits.co || '';
        DOM.get('#id_limit').value = bits.limit || '';

        yearsEl.style.display = 'none';
        dateEl.style.display = 'none';
        if((bits.timeframe === '=') && bits.date) {
            yearsEl.value = bits.date;
            yearsEl.style.display = 'inline-block';
        }
        else {
            if(bits.timeframe && bits.date) {
                dateEl.value = bits.date.format(DATE_FORMAT);
                dateEl.style.display = 'inline-block';
            }
        }
    };

    const loadLogs = (path) => {
        const m = path.match(/\/([^\/]+)\/?$/);
        if(m) {
            fetch(`/api/v1/logs/${m[1]}/`, (data) => {
                controller.initialize(data.entities, data.logs, {'mediaPrefix': ''})
            });
        }
    };

    return {
        fetch: fetch,
        loadLogs: loadLogs,
        parseHash: hash => HashBits.fromHash(hash),
        timeit: timeit,
        DOM: DOM,
        controller: controller,
    };
}(window));
