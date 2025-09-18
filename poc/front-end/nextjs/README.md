
# Next.js POC
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

tree -L 3 -I "node_modules"

.
├── app
│   ├── favicon.ico
│   ├── globals.css
│   ├── isRegisted      # Page after register
│   │   └── page.tsx
│   ├── layout.tsx
│   ├── login           # Login page
│   │   └── page.tsx
│   ├── page.tsx
│   └── register        # Register page
│       └── page.tsx
├── eslint.config.mjs
├── next.config.ts
├── next-env.d.ts
├── package.json         # Dependencies & scripts
├── package-lock.json
├── postcss.config.mjs
├── public              # Static assets
│   ├── file.svg
│   ├── globe.svg
│   ├── next.svg
│   ├── vercel.svg
│   └── window.svg
├── README.md
└── tsconfig.json

```