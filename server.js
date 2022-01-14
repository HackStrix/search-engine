const express = require('express'); 
const cors = require('cors'); 
// const JSON = require('json')
// const mongoose = require('mongoose'); 


require('dotenv').config(); 

const app= express(); 
const port = process.env.PORT || 5000; 

// const uri = process.env.ATLAS_URI; 
const uri = "mongodb+srv://admin:password1234$@web-map.qzzvr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
const words = ['python']

const MongoClient = require('mongodb').MongoClient;
const { resourceLimits } = require('worker_threads');





app.get('/api/search', (req,res)=>{
    const str = req.query.search
    const lst = [str]
    MongoClient.connect(uri, (err,db)=>{
        if (err) console.log(err); 
        console.log("we reached here 0")
        var dbo = db.db("web-map");
    
        dbo.collection("tags").find({'word':{'$in':lst}}).toArray((err,result)=>{
            console.log("we reached here 1")
            if (err) throw err; 
            let links = []
            console.log(result)
            console.log(typeof(result))
            result.map((obj)=>{
                // let bool;
                // try{
                //     JSON.parse(obj)
                //     console.log(true)
                // }
                // catch(e){
                //     console.log(false)
                // }
                for(var m in obj){
                    // console.log(m);
                    if(!isNaN(m)){
                        console.log(obj[m])
                        obj[m].map((url)=>{
                            links.push(url)
                        })
                    }
                }
                
                // for (var i in result){
                //     console.log(i)
                //     if(isNaN(i)){
                //         for (var j in result[i]){
                //             links.push(result[i][j])
                //         }
                //     }
                // }
                // var obj = eval('(' + result + ')');
                // for(var i in obj){
                //     console.log(i)
                //     links.push(obj[i])
                // }
            })
            
            console.log(links)
            links.map((url)=>{
                // console.log(url);
                var host = url.replace('http://','').replace('https://','').split(/[/?#]/)[0];
                console.log("we reached here 2")
                console.log(host)
                const list = [host]
                dbo.collection("domains").find({'url':{'$in':list}}).toArray((err, result)=>{
                    console.log(result)
                })
                console.log("we reached here 3")
                // console.log(obj)
            })
            res.send(result)
            db.close();
        })
    }); 
    
    // url/api/search?search=5
})

app.use(cors());
app.use(express.json()); 

app.listen(port, ()=> {

    console.log(`Server is running on port ${port}`); 
}); 
