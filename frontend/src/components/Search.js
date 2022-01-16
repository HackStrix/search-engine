import React from "react";
import { useHistory,Link } from "react-router-dom";
// import _ from "lodash";
// import faker from "faker";
// import React from "react";
// import { Search, Grid, Header, Segment } from "semantic-ui-react";



function Search({query, setQuery}) {
    const history = useHistory()

    function onSubmit(e){
        e.preventDefault();
        console.log('lol')
        console.log(e.target.value)
        console.log('query')
        history.push('/search');

        // useHistory.push('/search'); 
    }
    function onChange(e){
      console.log('yes')
      console.log(e.target.value)
      setQuery(e.target.value)
    }
  return (
    <div className="mb-3">
      <form>
        <label className="form-group">
          <input
            type="text"
            className="form-control"
            placeholder={query}
            onChange={(e)=>onChange(e)}
            name="search"
            required
          ></input>
          {/* <span className="border"></span> */}
        </label>
        <input className="button" type="submit" value='Submit'  onClick={(e)=>onSubmit(e)}>
          {/* <i className="zmdi zmdi-arrow-right"></i> */}
        </input>
      </form>
      {/* <input className="form-control form-control-lg" type="text" placeholder='search ' aria-label=".form-control-lg example" /> */}
    </div>
  );
}

export default Search;
