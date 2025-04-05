/** @type {import('prettier').Config} */

const config = {
  plugins: [require.resolve("@prettier/plugin-xml")],
  bracketSpacing: false,
  printWidth: 88,
  proseWrap: "always",
  semi: true,
  trailingComma: "es5",
  xmlWhitespaceSensitivity: "strict",
};

module.exports = config;
