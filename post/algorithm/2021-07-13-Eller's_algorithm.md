---
title:  "미로 생성 알고리즘"
excerpt: "미로 생성 알고리즘"

categories:
 algorithm
 
tags:
 [algorithm, maze]

toc: true
toc_sticky: true
date: 2021-07-13
---

# 미로 생성 알고리즘

학기 중에 미로 탐색 과제를 했었다. 주어진 미로의 최단경로와 그 개수를 탐색하는 DFS 알고리즘을 만들었다. 스택을 사용하여 길이 막힐 때마다 갈림길로 돌아오고, 도착점에 이르렀을 경우 다시 이전 갈림길로 돌아가 다른 길이 존재하는지, 존재한다면 이전의 경로보다 짧은지 탐색하는 알고리즘이었다. 더 이상 찾아볼 경로가 존재하지 않을 때 이 알고리즘은 종료된다. 

결과적으로 알고리즘은 잘 작동했다. 하지만 내가 만족스럽지 못했던 점은 알고리즘을 테스트할 수 있는 환경이 미리 주어진 미로 밖에 없었다는 점이다. 물론 미로를 약간 수정하여 입력할 수 있었지만 어디까지나 약간의 수정에 불과했고 더 큰 미로에서 얼마나 이 알고리즘이 잘 작동하는지 알고 싶었다. 그런 의미에서 완전히 무작위적인 미로를 만드는 방법을 알고 싶었다. 비록 그때는 시간에 쫒겨 구현하지 못했지만 이번 기회에 구현하게 되었다. 

## 종류

미로 생성 알고리즘에는 여러가지가 있다. Recursive backtracking, Eller's 알고리즘, 최소신장트리를 이용한 알고리즘, 이진트리 알고리즘 등. 각각의 특징을 간략하게 설명하자면 다음과 같다. 

1. Recursive backtracking: 구현이 간단하지만 재귀적 호출이 필요하다(물론 반복문으로 바꿀 수 있다).
2. Eller's 알고리즘: 구현이 복잡하고 이해하기 어렵지만, 무조건 선형시간에 미로를 생성하므로 가장 빠르다. 
3. 최소신장트리를 사용한 알고리즘: 구현이 간단하지만 이해하기가 약간 어렵고 짧은 막다른 길을 자주 생성한다. 
4. 이진트리 알고리즘: 경로에 편향이 존재하지만 구현이 간단하다. 

이번 프로젝트에서는 Eller의 알고리즘을 사용하여 미로를 생성하였다. 많은 수의 큰 미로를 생성하고 그 모두에 탐색 알고리즘을 돌려 성능을 알아보고 싶었기 때문에 빠르게 미로를 만드는 것이 중요하다고 생각했다. 

### Eller's Algorithm

그렇다면 Eller의 알고리즘의 순서를 정리해보자. 

1. 첫 행의 칸들을 모두 각각 다른 집합에 포함시킨다. 
2. 인접한 칸들을 무작위로 연결한다. 이때 연결한 칸들은 같은 집합으로 묶는다.
3. 현재 행의 모든 집합들은 적어도 하나의 아래 칸을 연결한다. 이 역시 같은 집합으로 묶는다. 
4. 다음 줄로 이동한다. 
5. 집합에 포함되지 않은 칸들을 각각 새로운 집합에 포함시킨다. 
6. 마지막 행이 아니라면 2부터 다시 반복한다. 
7. 마지막 행이라면, 다른 집합에 속한 칸들을 모두 같은 집합으로 연결한다. 

기본적인 정의는 위와 같지만 분명히 이해하기 어렵고 각 단계가 미로 생성에서 의미하는 바가 명확히 드러나지 않는다. 먼저 가장 중요한 전제부터 다루어보자. 

## 단계 분석

모든 벽의 초기 상태는 닫힘 상태이어야 한다. 그리고 인접한 두 칸이 같은 집합으로 묶이는 순간, 두 칸 사이의 벽은 열리게 된다. 이 때 조심해야 할 것은 벽이 열리는 조건은 '두 칸이 같은 집합으로 묶이는 순간'이라는 것이다. 자세한 이유는 아래에 설명하겠다. 

1. 만약 5x2 크기를 갖는 미로를 생성한다고 하자. 첫 행은 5칸으로 이루어져 있다. 1번 단계에 따라서 각 칸은 1번 집합, 2번 집합, 3번 집합, 4번 집합, 5번 집합에 포함된다. 같은 집합에 포함되는 인접한 칸은 존재하지 않으므로 열리는 벽도 없다. 
2. 무작위적으로 인접한 칸과 같은 집합으로 묶는다. 묶이는 순간 둘 사이의 벽도 열리게 된다. 각기 다른 집합에 속하던 칸들은 이제 2 2 3 4 4 이런 식으로 일부가 서로 같은 집합에 속하게 된다. 
3. 모든 집합은 적어도 하나의 아래 칸을 같은 집합으로 묶는다. 위의 예시에서 진행한다면 다음 행의 집합 상태는 아마 2 * 3 4 4 와 같은 상태일 것이다. * 으로 표시된 칸은 아직 집합에 할당하지 않은 칸이다. 
4. 다음 줄로 이동한다. 여기가 Eller의 알고리즘이 높은 성능을 보이는 이유인데, 한번 그린 행을 다시는 쳐다보지 않고 아래로 내려가기 때문이다. 이제 2 * 3 4 4 가 현재 행의 집합 상태가 된다. 
5. 현재 행에서 집합에 속하지 않은 칸, 즉 * 을 새로운 집합에 넣는다. 이미 없어진 집합인 1에 넣으면 2 1 3 4 4와 같다. 
6. 마지막 행이 아니라면 다시 2부터 진행한다. 
7. 편의상 2 1 3 4 4 가 마지막 행의 상태라고 가정해보자. 이대로 알고리즘이 끝난다면 1번 집합, 2번 집합, 3번 집합, 4번 집합은 서로 절대 만나지 않는 미로의 길이 될 것이다. 만약 중간에 만나는 길이 존재한다면 2번 단계에서 길이 열렸을 것이며, 같은 집합으로 묶였을 것이기 때문이다. 따라서 모든 길이 연결되도록 하기 위하여 다른 집합에 속한 칸들을 모두 이어준다. 
   1. 첫 번째 칸(2)와 두 번째 칸(1)을 이어준다. 따라서 두 칸의 집합은 모두 2가 된다. 
   2. 세 번째 칸(3)도 집합이 다르니 이어준다. 따라서 세 번째 칸 또한 2번 집합에 들어간다. 
   3. 네 번째 칸(4)도 같은 집합으로 묶는다. 이때 주의해야 하는데, 칸을 같은 집합으로 묶는다는 의미는 단순히 그 칸을 자신의 집합에서 꺼내어 현재 집합에 넣는다는 것이 아니다. 그 칸의 집합과 현재 집합 전체를 합병한다는 의미이다. 이 과정에서 단지 붙어있는 두 칸 사이의 벽 하나만 열릴 뿐이다. 따라서 네 번째 칸이 2번 집합에 들어감과 동시에 다섯 번째 칸도 2번 집합에 들어간다. 
   4. 네 번째 칸과 다섯 번째 칸은 가운데 닫힌 벽이 존재한다. 3번 과정에서 보다시피 두 칸은 가로로 서로 합병한 칸이 아니라 위의 4번 집합에서 동시에 내려왔을 뿐이기 때문이다. 따라서 가운데 벽이 여전히 존재하고 다만 바로 윗 행 때문에 서로 이어져 있으므로 같은 집합에 속하는 것이다. 따라서 두 칸은 모두 2번 집합에 속하기 때문에 둘 사이의 벽을 허물지 않고 그대로 넘어간다. 

이 모든 과정이 끝나면 결과적으로 모든 칸이 단 하나의 집합에 속하게 된다. 집합이 서로 달랐던 두 칸은 2번 과정에서 서로 합병되고, 마지막까지 달랐던 칸들은 7번 과정에서 같은 집합에 속하게 된다. 같은 집합에 속한 칸들은 반드시 서로 이어져 있다는 것을 생각하면, 이는 곧 모든 칸이 서로 이어져 있다는 뜻이다. 

여기에서 익숙함을 느낄 수 있는데, Eller의 알고리즘에서 '집합'이라는 개념은 곧 하나의 그래프를 뜻한다는 것을 알 수 있다. 서로 다른 집합을 합병하는 것은 서로 이어져 있지 않은 두 그래프를 연결하는 것과 같다. 두 그래프를 연결하는데 단 한개의 엣지면 충분하므로, 두 집합을 합병하는 것 역시 단 한개의 벽을 열기만 하면 된다. 

또한 미로 자체를 그래프로서 표현할 수 있는데, 이에 대해서는 [미로의 자료구조 포스트](https://altair823.com/post/data_structure/2021-07-13-maze_structure.html)에 자세히 적는다. 

## 복잡도 분석

놀랍게도 이 알고리즘은 윗 행을 전혀 참고하지 않는다. 단지 현재 행을 조작하고 다음 행의 집합을 미리 정하는 것이 전부이다. 모든 과정은 한 행씩 내려가며 진행된다. 따라서 칸 수에 대한 선형의 시간적 복잡도를 갖는다. 

## 구현

각 칸을 Set 컨테이너에 넣고 이에 대한 연산을 하는 것은 정의에 맞는 구현이지만, 각 사이클에서 이전 행의 정보를 필요로 하지 않는다는 것을 상기한다면 이는 분명 필요 이상의 오버헤드를 일으킨다. 한 행에 대응하는 1차원 정수형 배열 하나를 정의하고 특정 행에서 각 칸이 소속된 집합을 정수로 표현한다면 훨씬 가볍게 연산할 수 있을 것이다. 

그렇다면 집합 값은 몇까지 할당되는가? 한 행에서 각 칸에 할당할 수 있는 집합의 최대 개수는 곧 한 행에서 칸의 개수와 동일하다. 하지만 합병되어 없어진 집합 값을 추적하지 않는다면 새로 할당하는 집합 값은 충돌을 피하기 위해 앞에서 전혀 쓰이지 않았던 집합 값이 될 것이다. 조금 단순화해서 생각해본다면 할당되는 최대 집합 값은 미로 전체의 칸 수와 선형적으로 비례할 것이다. 작은 미로를 생성한다면 크게 의미 없겠지만 큰 미로를 생성한다면 더 이상 사용하지 않는 집합 값이 존재함에도 불구하고 오버플로우의 위험을 안고 있는 것이다. 

현재 사용 중인 집합 값을 Set 컨테이너에 저장하고 집합이 합병될 때마다 이를 갱신하도록 하였다. 집합을 할당할 때는 1부터 최대값까지 Set에 존재하지 않는 집합 값을 찾아 이를 할당하고 Set에 넣었다. 

필요한 것은 현재 행의 집합 값을 저장할 1차원 정수형 배열과 다음 행의 집합 값을 저장할 1차원 정수형 배열, 현재 사용 중인 집합 값을 저장할 집합이다. 이들을 사용하면 위에서 설명한 단계들을 구현하는데 큰 무리가 없을 것이다. 

## 마치며

무작위적인 미로를 빠르게 생성하는 Eller의 알고리즘을 살펴보았다. 이제 이를 바탕으로 다익스트라 알고리즘과 A*같은 여러 최단 경로 탐색 알고리즘을 테스트할 환경을 마련할 수 있었다. 

미로의 자료구조에 대한 자세한 내용은 [미로의 자료구조 포스트](https://altair823.com/post/data_structure/2021-07-13-maze_structure.html)에서 볼 수 있다. 

전제 소스 코드는 [MazeMaker](https://github.com/altair823/MazeMaker)에서 볼 수 있다. 

## 참고

[Maze Generation: Algorithm Recap](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap.html)

[Maze Generation: Eller's Algorithm](http://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm)



<script src="https://utteranc.es/client.js"
        repo="altair823/blog_comments"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>
