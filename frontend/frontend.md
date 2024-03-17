### Testing Frontend

To test frontend without docker, navigate to `./aibots-frontend` and run the following command:

```
npm install
npm run dev
```

Since NextJS only accepts environment variables from the immediate parent directory, do create a `.env.local` file with the following key:

```
NEXT_PUBLIC_API_ENDPOINT=...
```

You can view the frontend on `http://localhost:3000`