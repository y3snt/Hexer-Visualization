<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Hexer Visualization</h3>

  <p align="center">
    Visualization of an algorithm that solves XVI Polish Olympiad in Informatics (Stage III) problem - Hexer
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>

# 
#### Link to problem (ENG): https://www.oi.edu.pl/old/html/zadania/oi16/3/wietask.pdf
#### Link to problem (PL): https://www.oi.edu.pl/old/html/zadania/oi16/3/wie-1.pdf
<br />


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#required-modules">Required Modules</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

I found this problem so interesting, that I've decided to create animation that visualizes solution to the problem. I thinks it helps to understand the algorithm better by showing the path, not for just visited nodes, but for visited nodes with states (swords collected by Hexer at the moment of entering the node).

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

[![Python]][Next-url] 
#### v3.8.10

<p align="right">(<a href="#top">back to top</a>)</p>


## Required Modules 

##### Matplotlib
```sh
$ pip install matplotlib
```

##### Networkx
```sh
$ pip install networkx[default]
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ALGORITHM DESCRIPTION -->
## Algorithm

#### TL;DR Dijkstra + Bitmasks

The algorithm that solves the problem is modified Dijkstra. Instead of simply counting distances to every node from starting node (node 1 in this case) it counts distance to every node for every possible subset of swords that can be collected by Hexer. This sword subsets are stored in bit masks.

Initially all distances are set to infinity.
At the beggining 1-st node is added to the priority queue (with distance 0 and initial bitmask - swords collected in 1-st node).

Then this node (and every node that will be added to queue) is taken from the queue and processed: every neighbour of this node that we can enter to (by defeating monsters on the edge with currently collected swords) is checked; if the distance from current node to this neighbour is smaller than previous distance to the neighbour, we put this new distance to the queue with currently collected swords + swords collected by entering the neighbour (state for this neighbour node).

Additionally when node is processed it gets marked as processed, so it will be processed only once (for particular state).

When distance to n-th node is found or the queue is empty the algorithm stops.

##### This algorithm can be found in c++ or python version in the algorithms folder.

#### More information:

<p align="right">(<a href="#top">back to top</a>)</p>




<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Magdalena Doleśniak - magda.dolesniak@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
