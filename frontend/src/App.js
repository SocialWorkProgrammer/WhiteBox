import React from 'react';
import Header from './components/Header';
import Main from './components/Main';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Header />
      <Main />
      <Footer />
    </div>
  );
}

export default App;

// 아래의 형식을 사용할 수 도 있음.
// export default function App() {
//   return (
//     <h1 className='text-3xl font-bold underline'>
//       Start Project
//     </h1>
//   )
// }