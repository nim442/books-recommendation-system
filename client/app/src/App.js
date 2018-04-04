import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
         
          <h1 className="App-title">Book Recommendations</h1>
        </header>
        <div className="content">
          <div className="books">
            <div className="book">
              <div className="title">
                <img src="https://images.gr-assets.com/books/1436732693m/13496.jpg"></img>


              </div>
              <div className="description">
                <h4>Description</h4>
                <p>This is a description of a book</p>
              
              </div>
            </div>
            <div className="book">
              <div className="title">
                <img src=""></img>


              </div>
              <div className="description">
                <h4>Description</h4>
                <p>This is a description of a book</p>

              </div>
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
