# Design docs
Design docs are a critical way to communicate technical information, especially as we are all remote this quarter. Your goal with a design doc is to introduce a problem and explain, from a high level, how you plan to solve it. Here is an example of a real design doc that I wrote personally. After reading a design doc, people should understand what you’re doing and why, and enough of the details of how that they would come up with a reasonably similar implementation. Note: if you find yourself including code snippets in your design doc, then you are going into too much detail. Keep the discussion at a conceptual level and leave code for your pull requests.

Your design docs should be 1-2 pages long, written in Google docs, have comments from your teammates about any clarifications / suggestions / discussions, and contain the following:

* An introduction section, which is 2-3 paragraphs explaining the problem, from a high level, why it’s important and a sketch of the solution.

* An overview section for your solution. Go into some technical details here, but keep things at a conceptual level.

* A figure within your overview section to explain the main components of your system, the flow of information, or something else visually. Having a figure is absolutely critical and probably where you’ll spend most of your time (coming up with good figures is hard).

* A public interfaces section. If you’re working on a server component this includes APIs that you’re going to expose, or if you’re working on a module this includes any methods that other components will invoke, or if it’s a stand alone tool then the inputs and outputs for this tool. The most important part here is that you’re going to be working with other people so then need to know how to interact with what you write, but they don’t need to know how you implement these interfaces.