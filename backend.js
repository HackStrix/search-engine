// import fetch  from 'node-fetch';
const express = require('express'); 
const cors = require('cors'); 
const fetch = require('node-fetch');
const cheerio = require('cheerio');

async function getTitle(url) {
  // get html text from reddit
  const response = await fetch(url);
  // using await to ensure that the promise resolves
  const body = await response.text();

  // parse the html text and extract titles
  const $ = cheerio.load(body);
  const title = $("head > title").text().trim();
  console.log(title);
  return title;
  };


require('dotenv').config(); 

const app= express(); 
const port = process.env.PORT || 5000; 

const uri = process.env.ATLAS_URI; 
// const uri = "mongodb+srv://admin:<password>$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

// Create MongoDB client
const MongoClient = require('mongodb').MongoClient;
const client = new MongoClient(uri)

// Connecting to Database
try {
    client.connect()
}
catch(e){
    // Logging any connection error
    console.log(e)
}

// Specifying cors policy for frontend access.
// update to match the domain you will make the request from
// Middleware
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "https://vision-frontend.herokuapp.com", "http://vision-frontend.herokuapp.com"); 
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
  })


// The infamous Merge sort by HydroxyHelium
function merge(left, right) {
    let dbResults = []
    while (left.length && right.length) {
        
        if (left[0][1] > right[0][1]) {
            dbResults.push(left.shift())  
        } else {
            dbResults.push(right.shift()) 
        }
    }
    return [ ...dbResults, ...left, ...right ]
}

function mergeSort(array) {
  const half = array.length / 2
 
  if(array.length < 2){
    return array 
  }
  
  const left = array.splice(0, half)
  return merge(mergeSort(left),mergeSort(array))
}
// Merge Sort END



async function getData(wordList, dbWordTags, dbDomainCount, res, pageNumber) {
    let dbResults = await dbWordTags.find({'word':{'$in': wordList}}).toArray()
    let ratedLinks = {}
    let domainList = []
    let ratedDomains = {}
    let finalResults = []

    dbResults.map(async (obj)=>{

        for(var index in obj){
            if(!isNaN(index)){
                obj[index].map((url)=>{
                    if (ratedLinks[url])
                    {
                    ratedLinks[url] = ratedLinks[url]*index;
                    }
                    else{
                        ratedLinks[url]=index*1;
                    }
                }) 
            }
        }})
    // extract domain from links ... 
    for(var url in ratedLinks){
        var host = url.replace('http://','').replace('https://','').split(/[/?#]/)[0];
        domainList.push(host)
    }

    // Retrieve Domain Count from database
    let dbResultCount = await dbDomainCount.find({'url': {'$in':domainList}}).toArray()
    dbResultCount.map((obj)=>{
        ratedDomains[obj.url] = obj.count
    })
    
    // Assign appropriate Ratings according to the domainCount
    for(var index in ratedLinks){
        var host = index.replace('http://','').replace('https://','').split(/[/?#]/)[0];
        finalResults.push([index, Math.log(ratedLinks[index]*ratedDomains[host])])
    }
    // sort all the filtered queries
    finalResults = mergeSort(finalResults)
    
    // Only returning 20 results based on pageNumber
    let final = []
    const len = finalResults.length
    for (let step = 0; step < 20; step++) {
        if ((step*pageNumber) < len) {
            const val = finalResults[step*pageNumber]
            final.push([val[0],val[1]])

        }}
    console.log(final)
    res.send(final)
}

app.get('/api/search', async (req, res)=>{
    // Extracting Parameters from request
    const searchQuery = req.query.search;
    const pageNumber = req.query.page;

    // Splitting the search into multiple words.
    const wordList = searchQuery.split(" ")

    // Connecting to Database "web-map"
    var dbConn = client.db("web-map");

    // Running the algorithm
    getData(wordList, dbConn.collection("tags"), dbConn.collection("domains"), res,pageNumber)
})




app.use(cors());
app.use(express.json()); 

app.listen(port, ()=> {

    console.log(`Server is running on port ${port}`); 
}); 
