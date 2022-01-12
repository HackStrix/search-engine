const express = require('express'); 
const cors = require('cors'); 
const mongoose = require('mongoose'); 


require('dotenv').config(); 

const app= express(); 
const port = process.env.PORT || 5000; 

const uri = process.env.ATLAS_URI; 
const words = ['python']

const MongoClient = require('mongodb').MongoClient;





app.get('/api/search', (req,res)=>{
    const str = req.query.search
    const lst = [str]
    MongoClient.connect(uri, (err,db)=>{
        if (err) throw err; 
        var dbo = db.db("web-map");
    
        dbo.collection("tags").find({'word':{'$in':lst}}).toArray((err,result)=>{
            if (err) throw err; 
            console.log(result)
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
