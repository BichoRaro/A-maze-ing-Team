MIT License

Copyright (c) 2026 A-Maze-ing contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

---

## Why MIT for this project

This repository includes `mazegen`, a maze-generation module that is
explicitly meant to be reused as a dependency by later, unrelated projects
(see `mazegen/README.md`). The MIT License was chosen because it:

- Explicitly permits reuse, modification, and redistribution of the code,
  including in closed-source or commercial projects, as long as the
  original copyright notice is kept.
- Imposes no obligation on downstream projects to release their own source
  code (unlike copyleft licenses such as the GPL), which keeps `mazegen`
  easy to adopt as a dependency.
- Is short, widely understood, and compatible with virtually every other
  open-source license, minimizing friction for whoever builds on top of
  this work.