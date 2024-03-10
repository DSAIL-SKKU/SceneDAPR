import { ApolloClient, InMemoryCache, createHttpLink } from "@apollo/client";

// Create a new ApolloClient instance
const client = new ApolloClient({
  // Configure the HTTP link for GraphQL requests
  link: createHttpLink({
    // Set the URI for the GraphQL endpoint
    uri: process.env.REACT_APP_GRAPHQL_ENDPOINT,
  }),
  // Configure the cache for data storage
  cache: new InMemoryCache(),
});

// Export the ApolloClient instance as the default export
export default client;
