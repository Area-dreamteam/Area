# Vue.js POC
## Only front-end with a Login and Register Page

### Objective

- A simple login and register form
- No back-end connection and no database, API
- Basic page redirection with the path of the page when the user submit
- And a final page with Connect or Registed

### Installation and Run

```bash
npm install
npm run dev
```

### Project Structure
```
tree -L 3 -I "node_modules|dist"

.
├── env.d.ts
├── eslint.config.ts
├── index.html                # Main HTML entry
├── package.json              # Dependencies & scripts
├── package-lock.json
├── public                    # Static assets
│   └── favicon.ico
├── README.md
├── src                       # Main source code
│   ├── App.vue
│   ├── env.d.ts
│   ├── main.ts
│   ├── router
│   │   └── index.ts
│   └── views                 # Vue pages
│       ├── Home.vue
│       ├── isLogged.vue
│       ├── isRegisted.vue
│       ├── Login.vue
│       └── Register.vue
├── tsconfig.app.json
├── tsconfig.json             # TypeScript configuration
├── tsconfig.node.json
└── vite.config.ts            # Vite configuration

```