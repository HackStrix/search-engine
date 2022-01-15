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

  

//  function fetchTitle(url, onComplete = null) {
//     request(url, async function (error, response, body) {
//         var output = url; // default to URL

//         if (!error && response.statusCode === 200) {
//             const $ = await cheerio.load(body);
//             // console.log(`URL = ${url}`);
//             const title = $("head > title").text().trim();
//             console.log(title);
//             return title;
//             // console.log(`Title = ${title}`);
//             // output = `[${title}](${url})`;
//         } else {
//             console.log(`Error = ${error}, code = ${response.statusCode}`);
//         }

//         // console.log(`output = ${output} \n\n`);
//         if (onComplete)
//             onComplete(output);
//     });
// }


// const JSON = require('json')
// const mongoose = require('mongoose'); 


require('dotenv').config(); 

const app= express(); 
const port = process.env.PORT || 5000; 

// const uri = process.env.ATLAS_URI; 
// const uri = "mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
const uri = "mongodb://localhost:27017/"
const words = ['python']

const MongoClient = require('mongodb').MongoClient;
// const { resourceLimits } = require('worker_threads');
const client = new MongoClient(uri)

try {
    console.log('e')
    client.connect()
    console.log('f')
}
catch(e){
    console.log(e)
}

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "http://localhost:3000"); // update to match the domain you will make the request from
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
  })

function merge(left, right) {
    let arr = []
    while (left.length && right.length) {
        
        if (left[0][1] > right[0][1]) {
            arr.push(left.shift())  
        } else {
            arr.push(right.shift()) 
        }
    }
    return [ ...arr, ...left, ...right ]
}

function mergeSort(array) {
  const half = array.length / 2
 
  if(array.length < 2){
    return array 
  }
  
  const left = array.splice(0, half)
  return merge(mergeSort(left),mergeSort(array))
}

async function getData (clients, lst, db1, db2, res,pg) {
    let arr = await db1.find({'word':{'$in': lst}}).toArray()
    // console.log(arr)
    let links = {}
    let resultss = []
    let domains = {}
    let finalResults = []
    arr.map(async (obj)=>{

        for(var i in obj){
            if(!isNaN(i)){
                // console.log("hi")

                obj[i].map((url)=>{
                    console.log(url)
                    links[url] = i
                }) 
            }
        }})
    // console.log(links)  
    for(var url in links){
        // console.log(url)
        var host = url.replace('http://','').replace('https://','').split(/[/?#]/)[0];
        resultss.push(host)
    }
    // links.map(async([url, i])=>{
    //     var host = await url.replace('http://','').replace('https://','').split(/[/?#]/)[0];
    //     resultss.push(host)
        
    // })
    let result = await db2.find({'url': {'$in':resultss}}).toArray()
    result.map((obj)=>{
        domains[obj.url] = obj.count
    })
    for(var i in links){
        // const title = await getTitle(i)
        var host = i.replace('http://','').replace('https://','').split(/[/?#]/)[0];
        finalResults.push([i,links[i]*domains[host]])
    }

    finalResults = mergeSort(finalResults)
    let final = []
    const len = finalResults.length
    for (let step = 0; step < 20; step++) {
        // Runs 5 times, with values of step 0 through 4.
        if ((step*pg) < len) {
            const val = finalResults[step*pg]
            const title = await getTitle(val[0])
            final.push([val[0],val[1],title])

        }}
    // console.log(getTitle(''))
    res.send(final)
    // let result =  await arr.map(async (obj)=>{
    //         let links = []
    //         for(var i in obj){
    //             if(isNaN(i)){
    //                 await obj[i].map(async (url)=>{
    //                     links.push([url, i])
    //                 }) 
    //             }
    //         }
    //     })
    // )
}

app.get('/api/search', async (req, res)=>{
    const str = req.query.search;
    const pg = req.query.page;
    console.log(str)
    const lst = [str]
    console.log('here')
    var dbo = client.db("web-map");
    console.log("reached here")
    getData(client, lst, dbo.collection("tags"), dbo.collection("domains"), res,pg)
    // console.log(result)
    // res.send(result)
})




app.use(cors());
app.use(express.json()); 

app.listen(port, ()=> {

    console.log(`Server is running on port ${port}`); 
}); 
