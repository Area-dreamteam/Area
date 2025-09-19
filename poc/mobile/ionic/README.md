# Ionic (React) POC
## Only front-end with a Login and Register Page

### Objective

- A simple login and register form
- No back-end connection and no database, API
- Basic page redirection with the path of the page when the user submit
- And a final page with Connect or Registed

### Installation and Run

``` bash

# Fetch dependencies
npm install

# Run on a connected device or emulator
npm run dev
```

### Project Structure
```
tree -L 3 -I "node_modules"

.
├── capacitor.config.ts
├── cypress
│   ├── e2e
│   │   └── test.cy.ts
│   ├── fixtures
│   │   └── example.json
│   └── support
│       ├── commands.ts
│       └── e2e.ts
├── cypress.config.ts
├── eslint.config.js
├── index.html
├── ionic.config.json
├── package.json
├── package-lock.json
├── public
│   ├── favicon.png
│   └── manifest.json
├── src
│   ├── App.test.tsx
│   ├── App.tsx
│   ├── components
│   │   ├── ExploreContainer.css
│   │   └── ExploreContainer.tsx
│   ├── main.tsx
│   ├── pages
│   │   ├── home.css
│   │   ├── home.tsx
│   │   ├── isLogged.css
│   │   ├── isLogged.tsx
│   │   ├── isRegisted.css
│   │   ├── isRegisted.tsx
│   │   ├── login.css
│   │   ├── login.tsx
│   │   ├── register.css
│   │   └── register.tsx
│   ├── setupTests.ts
│   ├── theme
│   │   └── variables.css
│   └── vite-env.d.ts
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```