//https://soe6munsnjht7mfidvzdugcrpi.appsync-api.us-east-1.amazonaws.com/graphql
//graphql API key: da2-prokasn2cvdyzk337zjaj2nc5i
//https://lk7hjgsyz7.execute-api.us-east-1.amazonaws.com/dev

import {useState} from 'react'
import './App.css';
import {Amplify} from 'aws-amplify';
import { generateClient } from 'aws-amplify/api';
import config from './amplifyconfiguration.json';
import {listResults} from './graphql/queries'
import {updateResult, createResult} from './graphql/mutations'
import {StorageManager} from "@aws-amplify/ui-react-storage";
import {withAuthenticator, useAuthenticator, Button} from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/styles.css";

Amplify.configure(config);
const client = generateClient();

function App() {

  const {signOut} = useAuthenticator((context)=>[context.signOut])

  const [results, setResults] = useState([]);

  const [id, setId] = useState('');
  const [email, setEmail] = useState('');
  const [yourResult, setYourResult] = useState([
    [0,0.00],
    [0,0.00],
    [0,0.00],
    [0,0.00],
    [0,0.00],
    [0,0.00],
    [0,0.00],
    [0,0.00],
    [0,0.00],
  ]);
  const [bestScore, setBestScore] = useState('');

  const [alert, setAlert] = useState('');


  const fetchResults = async () => {
    try {
      const resultData = await client.graphql({query: listResults});
      const resultList = resultData.data.listResults.items;
      setResults(resultList)
    } catch (error) {
      console.log('error on fetching results', error);
    }
  }

  const updateAResult = async (idx, newResult) => {
    try {
      const result = results[idx];
      result.result = newResult;
      const myID = result.id;
      delete result.createdAt;
      delete result.updatedAt;
      const resultData = await client.graphql({
        query: updateResult, 
        variables: {
          input: {
            id: myID,
            result: newResult
          }

        }
      });
      const resultList = [...results]
      resultList[idx] = resultData.data.updateResult;
      setResults(resultList)
    } catch (error) {
      console.log('error on updating results for user', error);
    }
  };
  const createAResult = async (id, newResults) => {
    try {
      const result = results[0];
      result.id = id;
      result.result = results;
      delete result.createdAt;
      delete result.updatedAt;
      const resultData = await client.graphql({
        query: createResult, 
        variables: {
          input: {
            id: id,
            result: newResults
          }
        }
      });
      const resultList = [...results]
      resultList.push(resultData.data.createResult);
      setResults(resultList)
    } catch (error) {
      console.log('error on updating results for user', error);
    }
  };

  const handleEmailChange = (e) => {
    const val = e.target.value;
    setEmail(val);
  }
  const handleIdChange = (e) => {
    const val = e.target.value;
    setId(val);
  }

  function resultIntoArr(result){
    const rows = result.split(',');
    let trials = [];
    let howManyCorrect = 0;
    rows.forEach((row, rowIndex) => {
      const rowText = row.split(':');
      const rowSuccess = parseInt(rowText[0]); //0 or 1
      howManyCorrect += rowSuccess;
      const rowTime = parseFloat(rowText[1]);
      trials.push([rowSuccess,rowTime]);
    });
    trials.push([howManyCorrect,0.00]);

    return trials;
  }

  const handleSubmit = async () => {
    let emailGood = false;
    const emailStr = String(email)
    if(emailStr.length > 9){
      const domain = emailStr.substring(emailStr.length - 9);
      if(domain === '@sjsu.edu'){
        emailGood = true;
      } else {
        setAlert('not a valid email');
      }
    } else {
      setAlert('not a valid email');
    }

    let idGood = false;
    if(emailGood){
      if(String(id).length > 0){
        idGood = true;
      } else {
        setAlert('not a valid id');
      }
    }
    if(idGood){
      setAlert('grading')
      await setTimeout(10000);//10 seconds
      fetchResults();
      console.log('results',results)

      let currentResult = 'DNE';
      let currentResultIndex = -1;
      results.forEach((result, resultIndex) => {
        if(String(result.id) === id){ //we can update instead of create new
          currentResult = result.result;
          currentResultIndex = resultIndex;
        }
      });
      const newResult = results[results.length-1].result;
      if(newResult != 'abort'){
        if(currentResult == 'DNE'){ //if the current id doesn't exist in table, there is no other result yet
          console.log('DNE')
          createAResult(id, newResult);
          const newResultArr = resultIntoArr(String(newResult));
          setYourResult(newResultArr);
          setBestScore(String(newResultArr[8][0]));
        } else {
          console.log('did exist')
          const currentResultArr = resultIntoArr(String(currentResult));
          const newResultArr = resultIntoArr(String(newResult));
          console.log('newResult', newResultArr)
          console.log('currentResult', currentResultArr)
          setYourResult(newResultArr);
          if(newResultArr[8][0] > currentResultArr[8][0]){
            updateAResult(currentResultIndex, newResult); //it was greater, so update it
            setBestScore(String(newResultArr[8][0]));
          } else { //it was less
            setBestScore(String(currentResultArr[8][0]));
          }
        }
      } else {
        setAlert('aborted, code not good')
      }
      setAlert('graded');
    }
  
  }

  fetchResults()

  function numberResultToString(number){
    if(number == 1){
      return 'passed'
    }
    return 'failed'
  }

  return (
    <div className="App">
      
      <h1>Knight Attack </h1>
      <h2>Instructions</h2>
      <h3>A knight and a pawn are on a chess board. Can you figure out the minimum number of
moves required for the knight to travel to the same position of the pawn? On a single
move, the knight can move in an "L" shape; two spaces in any direction, then one space
in a perpendicular direction. This means that on a single move, a knight has eight
possible positions it can move to. (see end of document for a picture)
Write a function, knight_attack, that takes in 5 arguments:
n, kr, kc, pr, pc
n = the length of the chess board

kr = the starting row of the knight
kc = the starting column of the knight
pr = the row of the pawn
pc = the column of the pawn
The function should return a number representing the minimum number of moves
required for the knight to land on top of the pawn. The knight cannot move out of
bounds of the board. You can assume that rows and columns are 0-indexed. This
means that if n = 8, there are 8 rows and 8 columns numbered 0 to 7. If it is not possible
for the knight to attack the pawn, then return None.</h3>
      <h4 style={{ color: 'red' }}>Note: filename MUST be 'bfstest.py'. Any other filename will not be uploaded and the most recent attempt will be used instead.</h4>
      <h4 style={{ color: 'red' }}>Pressing SUBMIT without uploading a file will use the most recent attempt to grade.</h4>
      <StorageManager
      accessLevel="private"
      acceptedFileTypes={['bfstest.py']}
      maxFileCount={1}
      />
      <label>
        Email:
        <input name='emailInput' onChange={e => handleEmailChange(e)}/>
      </label>
      <label>
        ID:
        <input name = 'idInput' onChange={e => handleIdChange(e)}/>
      </label>
      <h2>{alert}</h2>
      
      <button onClick={handleSubmit}> SUBMIT </button>
      <h3>Test 1: {numberResultToString(yourResult[0][0])} Time: {yourResult[0][1]}</h3>
      <h3>Test 2: {numberResultToString(yourResult[1][0])} Time: {yourResult[1][1]}</h3>
      <h3>Test 3: {numberResultToString(yourResult[2][0])} Time: {yourResult[2][1]}</h3>
      <h3>Test 4: {numberResultToString(yourResult[3][0])} Time: {yourResult[3][1]}</h3>
      <h3>Test 5: {numberResultToString(yourResult[4][0])} Time: {yourResult[4][1]}</h3>
      <h3>Test 6: {numberResultToString(yourResult[5][0])} Time: {yourResult[5][1]}</h3>
      <h3>Test 7: {numberResultToString(yourResult[6][0])} Time: {yourResult[6][1]}</h3>
      <h3>Test 8: {numberResultToString(yourResult[7][0])} Time: {yourResult[7][1]}</h3>
      <h3>Best Score: {yourResult[8][0]}/8</h3>
      <Button onClick={signOut}>Sign Out</Button>
    </div>
  );
}

export default withAuthenticator(App);
