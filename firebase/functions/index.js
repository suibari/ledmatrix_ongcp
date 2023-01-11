const functions = require("firebase-functions");
const request = require('request');
const cheerio = require('cheerio');

// // Create and deploy your first functions
// // https://firebase.google.com/docs/functions/get-started
//
//exports.helloWorld = functions.https.onRequest((request, response) => {
//  functions.logger.info("Hello logs!", {structuredData: true});
//  response.send("Hello from Firebase!");
//});

exports.getNewsAndWeather = functions.https.onRequest(async (req, res) => {
  var result = {}

  result.news = await getNews();
  const weather = await getTemperatureAndWeather().then();
  result.temp = weather[0];
  result.weather = weather[1];

  res.send(result);
});

async function getNews() {
  return new Promise(resolve => {
    var atcl_arr = []
    const URL = "https://www.nikkei.com/news/category/"

    console.log("getting NEWS...")
    request(URL, (e, res, body) => {
      if (e) {
        console.error(e); 
      }
      try {
        const $ = cheerio.load(body);
        $('[class*="_titleL"]', '#CONTENTS_MAIN').each((i, elm) => {
          console.log($(elm).text());
          atcl_arr[i] = $(elm).text();
        });
        resolve(atcl_arr);
      } catch (e) {
        console.error(e);
      }
    })
  })
};

async function getTemperatureAndWeather() {
  return new Promise(resolve => {
    const URL = "https://tenki.jp/forecast/3/17/4610/14117/";

    console.log("getting weather information...");
    request(URL, (e, res, body) => {
    if (e) {
      console.error(e);
    }
    const $ = cheerio.load(body);
    var temp_tag = $('#rain-temp-btn');
    temp_tag.remove('.diff');
    const temp = temp_tag.text();

    const weather = $('p.weather-telop', '.today-weather').text();

    resolve([temp,weather]);
  });
  });
};