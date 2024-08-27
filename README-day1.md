# React
https://ko.react.dev/learn

**React 장점**

1. 컴포넌트 재상용성이 높음 : 각 컴포넌트에 전용 내부 로직과 렌더링 원칙을 부여할 수 있으며, 따로 구분되기 때문에, 만들어진 컴포넌트에 대한 활용성 및 재사용성이 높다.
2. 2022년 기준(너무 오래됐나?) Vue와 Angular의 거의 두 배이므로 그만큼 관련 정보가 인터넷에 많다.
3. 한국에서 좋아하는 프론트 프레임워크 : 취업공고를 보면 체감상 80% 이상이 React를 선호하고 있었으며, Vue를 주력 프레임워크를 사용하는 곳은 거의 없었다.
4. npm start를 입력하면 로컬 주소를 치지 않고도 자동으로 웹사이트에 띄워준다(Vue는 안해줌)


## React 기초
### import 하기

1. 만약 다른 곳에서 가져오고 싶다면 Vue처럼 import를 사용해서 가져오면 된다.

2. 단, 중괄호를 사용할 때가 있는데, export default가 아닌 단순 export function 등의 경우에 사용된다.

        ex : export default Counter() => import Counter from '../utils/1.js'

        ex2 : export function ChangeColor() => import { ChangeColor } from '../utils/2.js'

        import { useState } from 'react';
        import logo from './Logo.png';

### React 사용 시 자동 html 태그 사용이 안될 때
1. vscode 에디터에서 f1을 눌러 Open setting(JSON)을 연다.
2. 아래에 emmet.includeLanguages가 있을텐데, 거기에 "javascript": "javascriptreact"를 집어넣는다.

    "emmet.includeLanguages": {
        "django-html": "html",
        "javascript": "javascriptreact" <- 이 부분!
        },

### React 컴포넌트는 항상 대문자로 시작해야 함

### React 컴포넌트에 CSS 집어넣는 방법
1. props를 사용한 후 최상위 컴포넌트에 해당 classsName을 넣기

2. 해당 컴포넌트에 바로 className을 넣기

3. 최상위 컴포넌트에 바로 className은 못 들어간다!
