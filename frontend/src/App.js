import React from 'react';
import './App.css';
import { Query } from 'react-apollo';
import { gql } from 'apollo-boost';


function App() {
  return (
    <div className="App">
        <p>
          Main Component
        </p>
        <Query query={GET_CATEGORIES_QUERY}>
            {
                ({data, loading, error}) => {
                    if (loading) return <div>Loading</div>
                    if (error) return <div>Error</div>

                    return (
                        <div>
                            {JSON.stringify(data)}
                        </div>
                    )
                }
            }
        </Query>
    </div>
  );
}

const GET_CATEGORIES_QUERY = gql`
    {
      allCategories {
        id,
        name
      }
    }
`

export default App;
