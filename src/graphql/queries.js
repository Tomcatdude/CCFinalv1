/* eslint-disable */
// this is an auto generated file. This will be overwritten

export const getResult = /* GraphQL */ `
  query GetResult($id: ID!) {
    getResult(id: $id) {
      id
      createdAt
      updatedAt
      result
      __typename
    }
  }
`;
export const listResults = /* GraphQL */ `
  query ListResults(
    $filter: ModelResultFilterInput
    $limit: Int
    $nextToken: String
  ) {
    listResults(filter: $filter, limit: $limit, nextToken: $nextToken) {
      items {
        id
        createdAt
        updatedAt
        result
        __typename
      }
      nextToken
      __typename
    }
  }
`;
