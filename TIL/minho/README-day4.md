# React
https://ko.react.dev/learn
  
### 데이터 표시하기
1. JSX를 이용하여 마크업을 넣기

        const user = [
          {name : 민호, id : 1, phone : 010-0000-0000},
        ]
        
        return (
          <h1>
          {user.name} // 민호
          </h1>
        )
=> user라는 변수를 선언 후, 그 안에 딕셔너리의 키 값을 중괄호 + 변수이름.키이름을 통해 나타낼 수 있음.

### 조건부 렌더링
조건문은 if문을 통해 실행한다는 점에서 자바스크립트와 같음. 삼항 연산자도 가능함.

        let content; // 일반 조건문
          if (isLoggedIn) {
            content = <AdminPanel />;
          } else {
            content = <LoginForm />;
          }
          return (
            <div>
              {content}
            </div>
          );

        <div> // 삼항연산자
          {isLoggedIn ? (
            <AdminPanel />
          ) : (
            <LoginForm />
          )}
        </div>

        // else가 없는 경우 &&를 이용하면 한 줄로 끝남
        <div>
        {isLoggedIn && <AdminPanel />} // <= 만약 로그인이 되어있다면 AdminPanel 컴포넌트를 보여줘라!!
        </div>


### 리스트 렌더링하기
   컴포넌트 리스트를 렌더링하기 위해서 for문이나 map 함수를 이용할 수 있다.
   ```
        // 리스트
        const products = [
          { title: 'Cabbage', id: 1 },
          { title: 'Garlic', id: 2 },
          { title: 'Apple', id: 3 },
        ];
        // 실제 함수
        const listItems = products.map(product =>
        // listITtems란 변수를 선언 후, products를 product로 나눔
          <li key={product.id}>
            {product.title}
          </li>
        );
        // 실제 return은 listItems변수를 선언
        return (
          <ul>{listItems}</ul>
        );

  ```

### 이벤트에 응답하기
함수 안에 다시 이벤트핸들러 함수를 선언하면 컴포넌트 안에 이벤트를 생성할 수 있다!
```
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }

  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```

### 화면 업데이트하기
컴포넌트가 특정 정보를 '기억'하도록 만들기 위해서는 해당 컴포넌트에 state를 추가하면 됨.
```
import { useState } from 'react';

export default function MyApp() {
  return (
    <div>
      <h1>Counters that update separately</h1>
      <MyButton />
      <MyButton />
    </div>
  );
}

function MyButton() {
  const [count, setCount] = useState(0);
  // 여기 잘 보면 count와 setCount 두 개가 들어가는 것을 볼 수 있는데,
  // 첫번째 count는 현재 state, setCount는 count를 업데이트하는 함수이다.
  function handleClick() {
    // count + 1을 setCount 함수에 담으면 된다.
    setCount(count + 1);
  }

  return (
    <button onClick={handleClick}>
      Clicked {count} times
    </button>
  );
}

```

### 컴포넌트 간 데이터 공유
```
import { useState } from 'react';

export default function MyApp() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <div>
      <h1>Counters that update together</h1>
      <MyButton count={count} onClick={handleClick} />
      <MyButton count={count} onClick={handleClick} />
    </div>
  );
}

function MyButton({ count, onClick }) {
  return (
    <button onClick={onClick}>
      Clicked {count} times
    </button>
  );
}

```