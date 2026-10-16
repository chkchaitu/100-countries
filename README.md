# World Atlas for Indian passport holders (100 Countries goal)

A static, interactive atlas for Indian passport holders: low-budget multi-country trips, visa rules, best months, day-by-day plans and unique experiences.

**Status:** early version. The atlas covers 195 countries: the 181 that the 34 trips cover (18 researched core trips and 16 rough draft trips) plus 14 popular hub countries. Each has a visa rule for an Indian passport with sources and a check date, and a profile with places, best months, budget, transport and cautions. Experiences and records lists are still partial. Prices, visa rules and opening hours are estimates from research on 16 October 2026 and must be confirmed with official sources before booking. This is not legal, visa or travel advice.

## Live site

https://world.chaitu.in/ (the old address chkchaitu.github.io/100-countries/ redirects here).

## Run it locally

Serve the folder with any static server (for example `python3 -m http.server`) and open it in a browser. The page loads its data from the `data/` folder, so opening `index.html` directly from disk will not work. There is no build step.

## Privacy

Nothing a visitor ticks (visited countries, plan, visas) leaves their browser. It is stored in `localStorage` only.

## Data and sources

Map shapes come from Natural Earth via the `world-atlas` package (public domain). Content is rewritten from research with sources recorded per item; add a source link and a "last checked" date to every record before publishing it.

## Contributing

Issues and pull requests that correct a fact should include an official source link.

## What each country page shows

Flag and currency, visa rule for an Indian passport, how to apply (official links, documents, photo, fee) or the visa-free entry conditions, transit rules, places, best months, budget, transport, unique experiences, cautions, vaccinations and health, and what to do when returning to India. Items marked unverified could not be confirmed on an official page.

## Vision

The goal today is to help people who dream of visiting 100 countries. The aim is a one-stop planner for anyone travelling from India to any country in the world: visa requirements, places to visit, itineraries, best months, budgets and practical tips, all with sources and a last-checked date. Countries are added a few at a time.
