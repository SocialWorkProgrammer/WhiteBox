# 자바스크립트의 비동기방식
- 자바스크립트의 비동기 방식은 코드가 블로킹 없이 실행되도록 하는 중요한 특성
- 비동기 처리는 자바스크립트가 단일 스레드로 동작하면서도 빠르고 효율적으로 작업을 처리할 수 있도록 함
- 비동기 방식은 시간이 오래 걸리는 작업(예: 파일 읽기, API 호출, 타이머 등)을 수행할 때 메인 스레드가 멈추지 않고 계속해서 다른 작업을 처리할 수 있도록 해줌
  
### 비동기 처리의 주요 방식
1. 콜백 함수(Callback Functions)
   비동기 작업이 완료되었을 때 호출되는 함수. 단, 콜백 함수가 중첩될 경우 콜백 지옥이 발생할 수 있음

        console.log('Start');

        setTimeout(() => {
        console.log('This runs after 2 seconds');
        }, 2000);

        console.log('End');

        a. start 출력 
        b. End 출력, 
        c. This runs after 2seconds 출력
=> 왜 중간에 있는 것이 마지막에 나왔는가? 2초 뒤 실행하도록 setTimeout을 설정했기 때문.

=> 이러한 면을 고려했을 때 이런 비동기 방식을 잘 활용하면 내가 원하는대로 작업 순서를 지정할 수 있다는 장점이 존재함.

2. Promise
   'Promise'는 비동기 작업의 성공(fulfilled) 또는 실패(rejected)를 나타내는 객체. 'then'과 'catch'를 이용하여 작업의 결과를 처리할 수 있음

        const fetchData = () => {
        return new Promise((resolve, reject) => {
          setTimeout(() => {
            resolve('Data fetched');
            }, 1000);
          });
        };

        fetchData()
        .then(data => console.log(data))
        .catch(error => console.error(error));

3. async/await
   async/await는 Promise를 더 간단하고 읽기 쉬운 방식으로 사용할 수 있게 해줌
   await는 Promise가 해결될 때까지 기다려줌.

        const fetchData = async () => {
          try {
            const data = await new Promise((resolve, reject) => {
              setTimeout(() => {
                resolve('Data fetched');
              }, 1000);
            });
          console.log(data);
          } catch (error) {
        console.error(error);
        }
        };

        fetchData();
