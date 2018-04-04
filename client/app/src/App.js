import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import 'isomorphic-fetch';

class App extends Component {
  constructor(props) {
    super(props)
    this.getData()
  }
  getData(){
    fetch('http://localhost:5555/get_knn')
      .then(response => response.json())
      .then(data => {
        this.setState({  books: data['books'], loading: false });

      });
  }
  render() {
    console.log(this.state)
    if(this.state!=null){
      var book=this.state['books'].map(b=>{
        book=b[0]
        return <div className="book">
          <div className="title">
            <img src={book['image_url']}></img>
            <div className="title-author">
              <h4>{book['title_without_series']}</h4>
              <p>by {book['authors']['author']['name']}</p>

            </div>



          </div>
          <div className="description">
            <h4>Description</h4>
            <p dangerouslySetInnerHTML={{ __html: book['description'] }}></p>
          </div>
        </div>


      });
    }
    return (
      <div className="App">
        <header className="App-header">
         
          <h1 className="App-title">Book Recommendations</h1>
        </header>
        <div className="content">
        <div className="books-scroll">
          <div className="books">
            {book}
           
          
          </div>
          </div>
          <div id="graph">
          </div>
        </div>
      </div>
    );
  }
}

export default App;
