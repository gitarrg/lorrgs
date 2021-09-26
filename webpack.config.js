
// Imports
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const path = require("path")

// Constants
const DEBUG = process.env.NODE_ENV !== "production";


// Config
module.exports = {

    mode: process.env.NODE_ENV || 'development',

    entry: [
        path.resolve(__dirname, "lorgs/static/main.js"),
        path.resolve(__dirname, "lorgs/templates/scss/main.scss"),
    ],

    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",   // Translates CSS into CommonJS
                    "sass-loader"   // Compiles Sass to CSS
                ]
            }
        ]
    },

    output: {
        path: path.resolve(__dirname, "lorgs/static/_generated"),
        filename: `main.js`,
    },

    // for testing
    optimization: {
        minimize: process.env.NODE_ENV == "production",
        minimizer: [new TerserPlugin({
            terserOptions: {
                compress: {
                    drop_console: true,
                }
            }
        })],
    },

    plugins: [
        new MiniCssExtractPlugin({
            filename: "style.css",
        }),
    ],

}
