import React from 'react'; 
import axios from "axios";
import { useState, useEffect } from 'react';
import Search from './Search';


function Results({search}) {

    const [post,setPost] = useState([]); 

    const params = new URLSearchParams([['search',search]]);

    useEffect(()=> axios.get('http://127.0.0.1:5000/api/search',{ params }).then((response) => {
        setPost(response.data);
      }),[]);


    return (
        <div>
            hello
            {console.log(search)}
            {console.log(post)}

        </div>
    )
}

export default Results

