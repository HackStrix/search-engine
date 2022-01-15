// import bg from './images/background.png';
import './App.css';
// import { BrowserRouter } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Search from './components/Search';
import {
  Route,
  Link
} from 'react-router-dom';



import Results from './components/Results';

function App() {

  const [query,setQuery]=useState('');


  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={bg} className="" alt="logo" /> */}
        {/* hello world */}
        {/* <Search /> */}
        <Route exact path="/">
          <Search
            query = {query}
            setQuery = {setQuery}
          />
        </Route>

        <Route path="/search">
          <Results
            search = {query}
          />
        </Route>


        {/* <Route path="/search" component={Results
        query = {query}
        setQuery = {}
        }/> */}
        
      </header>
    </div>
  );
}

export default App;
