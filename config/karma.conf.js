module.exports = function(config){
  var opalPath = process.env.OPAL_LOCATION;
  var karmaDefaults = require(opalPath + '/opal/tests/js_config/karma_defaults.js');
  var baseDir = __dirname + '/..';
  var coverageFiles = [
    __dirname+'/../pathology/static/js/pathology/**/*.js',
  ];
    var includedFiles = [
      __dirname+'/../pathology/static/js/pathology/**/*.js',
      __dirname+'/../pathology/static/js/test/**/*.js',
  ];

  var defaultConfig = karmaDefaults(includedFiles, baseDir, coverageFiles);
  config.set(defaultConfig);
};