const StringReplacePlugin = require("string-replace-webpack-plugin");

module.exports = {
  pluginOptions: {
    electronBuilder: {
      outputDir: "dist",
      builderOptions: {
        productName: "Simulatant",
        compression: "normal",  // "store": fast build, "normal": smaller executeable
        portable: {
            splashImage: "logo\\splash.bmp"
          },
        extraResources: [
          {
            from: "dist/simulserver",
            to: "simulserver",
            filter: "**/*"
          }
        ],
        win: {
          target: "portable"
        }
      }
    }
  },
  chainWebpack: config => {
    config.module
      .rule("plotly")
      .test(/plotly\.js$/)
      .use("stringreplace")
      .loader(
        StringReplacePlugin.replace({
          replacements: [
            {
              pattern: /module.exports = d3; else this.d3 = d3;\n}\(\);/,
              replacement: function() {
                return "module.exports = d3; else this.d3 = d3;\n}.apply(self);";
              }
            }
          ]
        })
      )
      .end();
  }
};
