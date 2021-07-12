---
sort: 3
title: '트랜스미션 &#8220;Permission denied&#8230;&#8221; 오류 해결하기'
date: 2021-03-02T16:00:59+09:00
author: altair823
categories:
  - 라즈베리파이
---
<img src="https://user-images.githubusercontent.com/46125008/123520657-9d066500-d6ec-11eb-8a72-3f0d2c95f995.png">

정리하자면 &#8220;Permission&#8221; 오류는 토렌트로 받은 파일을 저장할 공간의 권한 문제로 발생하는 오류라는 것이다. 다운로드 할 목적지 폴더와 트랜스미션의 사용자를 맞춰주면 된다. 모든 권한을 열고 트랜스미션의 유저 이름을 root로 하는 것도 방법이지만 블로그 서버도 돌아가는 라즈베리파이의 보안을 신경쓰지 않을 수 없다. 따라서 폴더의 소유자와 그 권한을 바꾸는 작업을 했다.

### 권한의 이해

<img src="https://user-images.githubusercontent.com/46125008/123520656-9d066500-d6ec-11eb-8274-c0106543e204.png"> 

ssh로 접속하여 ls -al로 확인한 전체 폴더들의 권한들이다. 맨 앞의 d는 디렉터리, 즉 폴더라는 뜻이다. 그 뒤로 나타나는 r, w, x는 각각 read, write, execute, 그러니까 읽기권한, 쓰기권한, 실행권한이라는 뜻이다. d (단일 파일이라면 -)이후의 부분은 세 개씩 잘라 읽으면 되는데, 앞에서부터 \[소유자의 권한\]\[그룹의 권한\][그 외 사용자의 권한]을 뜻한다.

또한 s와 t는 특수권한을 뜻하는데, 소유자 권한에 붙으면 해당 파일의 접근 권한을 다른 사용자가 잠시 빌려올 수 있도록 허용하는 것이다. 그룹 권한에 붙으면 역시 파일의 접근 권한을 그룹에서 다른 사용자가 잠시 빌려올 수 있다. 이 두 경우 x대신 s가 들어가게 된다. 그 외의 사용자 권한에 특수권한이 붙으면 x대신 t가 붙게 되며 이는 파일의 생성은 누구나 가능하지만 삭제는 생성한 사람과 소유자만 가능하게 하는 옵션이다.

따라서 위에 보이는 문자들을 해석해보면

d rwx rws r-x :

  1. 이는 폴더이며,
  2. 소유자(root)에게 모든 권한을 주고 있고,
  3.  해당 그룹(user)에게 역시 모든 권한을 주고 있으며,
  4. 다른 사용자들은 읽기와 실행만 가능하다.
  5. 하지만 소유 그룹의 파일을 실행해야 할 경우 해당 그룹의 권한을 빌려 다른 사람이 실행할 수 있다.

### 해결

권한의 종류들을 알았으니 이제 폴더의 권한을 바꿔줄때다. chmod로 파일의 권한을, chown으로 소유자과 그룹을 바꿀 수 있다. 먼저 트랜스미션을 정지한다.

<pre class="EnlighterJSRAW" data-enlighter-language="generic" data-enlighter-theme="godzilla" data-enlighter-linenumbers="false">sudo service transmission-daemon stop</pre>

트랜스미션의 유저 이름은 debian-transmission이다. 따라서

<pre class="EnlighterJSRAW" data-enlighter-language="generic" data-enlighter-theme="godzilla" data-enlighter-linenumbers="false">sudo chown -R Debian-transmission (토렌트 파일을 저장할 폴더명, 또는 경로)/</pre>

를 입력해 소유자를 바꾸면 된다. 여기서 옵션으로 준 -R은 하위 폴더와 파일들의 권한까지 일괄적으로 변경하는 옵션이다. 만약 이렇게 했는데도 권한오류가 발생한다면

<pre class="EnlighterJSRAW" data-enlighter-language="generic" data-enlighter-theme="godzilla" data-enlighter-linenumbers="false">sudo chmod -R 777 (토렌트 파일을 저장할 폴더명, 또는 경로)/</pre>

를 입력해 권한을 바꿔주면 된다. 이렇게 하면 소유자나 소유 그룹 뿐만 아니라 다른 사용자도 폴더에 접근해 쓰기를 할 수 있다. 이제 트랜스미션을 다시 실행한다.

<pre class="EnlighterJSRAW" data-enlighter-language="generic" data-enlighter-theme="godzilla" data-enlighter-linenumbers="false">sudo service transmission-daemon start</pre>

다시 토렌트 파일들을 넣어 확인해보면 정상적으로 작동하는 것을 볼수 있을 것이다.

<script src="https://utteranc.es/client.js"
        repo="altair823/blog_comments"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>