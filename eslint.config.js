export default [
  {
    ignores: [
      "node_modules/**",
      "dist/**",
      "build/**",
      "coverage/**",
      ".git/**",
    ],
  },

  {
    files: ["**/*.{js,mjs,cjs}"],

    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        console: "readonly",
        process: "readonly",
        Buffer: "readonly",

        __dirname: "readonly",
        __filename: "readonly",
        module: "readonly",
        require: "readonly",
        exports: "readonly",

        window: "readonly",
        document: "readonly",
        fetch: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
      },
    },

    rules: {
      // Likely bugs
      "no-undef": "error",
      "no-redeclare": "error",
      "no-unreachable": "error",
      "no-fallthrough": "error",
      "no-global-assign": "error",
      "no-import-assign": "error",
      "no-loss-of-precision": "error",
      "no-self-assign": "error",
      "no-self-compare": "error",
      "no-constant-condition": "warn",
      "no-cond-assign": "error",
      "valid-typeof": "error",
      "use-isnan": "error",

      // Suspicious or confusing code
      "no-unused-vars": "warn",
      "no-useless-return": "warn",
      "no-useless-catch": "warn",
      "no-useless-concat": "warn",
      "no-useless-escape": "warn",
      "no-useless-rename": "warn",
      "no-duplicate-imports": "warn",
      "no-var": "warn",
      "prefer-const": "warn",
      "prefer-template": "warn",

      // Beginner-friendly code quality
      eqeqeq: "warn",
      curly: "warn",
      "default-case": "warn",
      "no-else-return": "warn",
      "no-lonely-if": "warn",
      "no-nested-ternary": "warn",
      "no-multi-assign": "warn",

      // Maintainability / readability
      complexity: ["warn", 10],
      "max-depth": ["warn", 4],
      "max-nested-callbacks": ["warn", 3],
      "max-params": ["warn", 5],
      "max-lines-per-function": [
        "warn",
        {
          max: 80,
          skipBlankLines: true,
          skipComments: true,
        },
      ],

      // Keep these off to avoid noisy style feedback
      semi: "off",
      quotes: "off",
      indent: "off",
      "comma-dangle": "off",
      "no-console": "off",
    },
  },

  {
    files: ["**/*.cjs"],
    languageOptions: {
      sourceType: "commonjs",
    },
  },
];
