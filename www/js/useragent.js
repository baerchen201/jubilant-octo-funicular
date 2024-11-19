var regexps = require("./lib/regexps");

// UserAgent parsers:
var agentparsers = regexps.browser,
  agentparserslength = agentparsers.length;

/**
 * The representation of a parsed user agent.
 *
 * @constructor
 * @param {String} family The name of the browser
 * @param {String} major Major version of the browser
 * @param {String} minor Minor version of the browser
 * @param {String} patch Patch version of the browser
 * @param {String} source The actual user agent string
 * @api public
 */
function Agent(family, major, minor, patch, source) {
  this.family = family || "Other";
  this.major = major || "0";
  this.minor = minor || "0";
  this.patch = patch || "0";
  this.source = source || "";
}

/*** Generates a string output of the parsed user agent.
 *
 * @returns {String}
 * @api public
 */
Agent.prototype.toAgent = function toAgent() {
  var output = this.family,
    version = this.toVersion();

  if (version) output += " " + version;
  return output;
};

/**
 * Generates a string output of the parser user agent and operating system.
 *
 * @returns {String}  "UserAgent 0.0.0 / OS"
 * @api public
 */
Agent.prototype.toString = function toString() {
  var agent = this.toAgent(),
    os = this.os !== "Other" ? this.os : false;

  return agent + (os ? " / " + os : "");
};

/**
 * Outputs a compiled veersion number of the user agent.
 *
 * @returns {String}
 * @api public
 */
Agent.prototype.toVersion = function toVersion() {
  var version = "";

  if (this.major) {
    version += this.major;

    if (this.minor) {
      version += "." + this.minor;

      // Special case here, the patch can also be Alpha, Beta etc so we need
      // to check if it's a string or not.
      if (this.patch) {
        version += (isNaN(+this.patch) ? " " : ".") + this.patch;
      }
    }
  }

  return version;
};

/**
 * Check if the userAgent is something we want to parse with regexp's.
 *
 * @param {String} userAgent The userAgent.
 * @returns {Boolean}
 */
function isSafe(userAgent) {
  var consecutive = 0,
    code = 0;

  for (var i = 0; i < userAgent.length; i++) {
    code = userAgent.charCodeAt(i);
    // numbers between 0 and 9, letters between a and z
    if ((code >= 48 && code <= 57) || (code >= 97 && code <= 122)) {
      consecutive++;
    } else {
      consecutive = 0;
    }

    if (consecutive >= 100) {
      return false;
    }
  }

  return true;
}

/**
 * Parses the user agent string with the generated parsers from the
 * ua-parser project on google code.
 *
 * @param {String} userAgent The user agent string
 * @param {String} [jsAgent] Optional UA from js to detect chrome frame
 * @returns {Agent}
 * @api public
 */
function parse(userAgent, jsAgent) {
  if (!userAgent || !isSafe(userAgent)) return new Agent();

  var length = agentparserslength,
    parsers = agentparsers,
    i = 0,
    parser,
    res;

  for (; i < length; i++) {
    if ((res = parsers[i][0].exec(userAgent))) {
      parser = parsers[i];

      if (parser[1]) res[1] = parser[1].replace("$1", res[1]);
      if (!jsAgent)
        return new Agent(
          res[1],
          parser[2] || res[2],
          parser[3] || res[3],
          parser[4] || res[4],
          userAgent
        );

      break;
    }
  }

  // Return early if we didn't find an match, but might still be able to parse
  // the os and device, so make sure we supply it with the source
  if (!parser || !res) return new Agent("", "", "", "", userAgent);

  // Detect Chrome Frame, but make sure it's enabled! So we need to check for
  // the Chrome/ so we know that it's actually using Chrome under the hood.
  if (
    jsAgent &&
    ~jsAgent.indexOf("Chrome/") &&
    ~userAgent.indexOf("chromeframe")
  ) {
    res[1] = "Chrome Frame (IE " + res[1] + "." + res[2] + ")";

    // Run the JavaScripted userAgent string through the parser again so we can
    // update the version numbers;
    parser = parse(jsAgent);
    parser[2] = parser.major;
    parser[3] = parser.minor;
    parser[4] = parser.patch;
  }

  return new Agent(
    res[1],
    parser[2] || res[2],
    parser[3] || res[3],
    parser[4] || res[4],
    userAgent
  );
}

/**
 * Does a more inaccurate but more common check for useragents identification.
 * The version detection is from the jQuery.com library and is licensed under
 * MIT.
 *
 * @param {String} useragent The user agent
 * @returns {Object} matches
 * @api public
 */
function is(useragent) {
  var ua = (useragent || "").toLowerCase(),
    details = {
      chrome: false,
      firefox: false,
      ie: false,
      mobile_safari: false,
      mozilla: false,
      opera: false,
      safari: false,
      webkit: false,
      android: false,
      version: (ua.match(exports.is.versionRE) || [0, "0"])[1],
    };

  if (~ua.indexOf("webkit")) {
    details.webkit = true;

    if (~ua.indexOf("android")) {
      details.android = true;
    }

    if (~ua.indexOf("chrome")) {
      details.chrome = true;
    } else if (~ua.indexOf("safari")) {
      details.safari = true;

      if (~ua.indexOf("mobile") && ~ua.indexOf("apple")) {
        details.mobile_safari = true;
      }
    }
  } else if (~ua.indexOf("opera")) {
    details.opera = true;
  } else if (~ua.indexOf("trident") || ~ua.indexOf("msie")) {
    details.ie = true;
  } else if (~ua.indexOf("mozilla") && !~ua.indexOf("compatible")) {
    details.mozilla = true;

    if (~ua.indexOf("firefox")) details.firefox = true;
  }

  return details;
}

/**
 * Parses out the version numbers.
 *
 * @type {RegExp}
 * @api private
 */
is.versionRE = /.+(?:rv|it|ra|ie)[\/: ]([\d.]+)/;
