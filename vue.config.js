const StringReplacePlugin = require("string-replace-webpack-plugin");

module.exports = {
  pluginOptions: {
    electronBuilder: {
      outputDir: "dist"
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
