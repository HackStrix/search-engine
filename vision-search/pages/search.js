import Head from 'next/head';
import React,{ useState, useEffect } from 'react';
import axios from 'axios'
import { useRouter } from 'next/router';

export default function Search(){
    const [post,setPost] = useState([]); 
    // console.log(context.params)
    const router = useRouter()
    console.log(router)
    const {
      query: { search },
    } = router
    console.log(search)
    const params = new URLSearchParams([['search',search],['page',1]]);

    useEffect(()=> axios.get('http://127.0.0.1:5000/api/search',{ params }).then((response) => {
        console.log(response.data)
        setPost(response.data);
      }),[]);
    return (
        <div className="flex flex-col ml-96 my-32 justify-center text-left">
            <h1 className="text-5xl font-lg font-mono leading-tight text-blue-400">Results</h1>
            {/* <ol> */}
                {post.map((x)=>{
                    return <div className="text-white my-4 text-xl" key="1"><a href={x[0]}>{x[0]}</a></div>
                })}
            {/* </ol> */}
        </div>
    )
};