# C++11 Lambda表达式学习笔记

## 参考资料

- [知乎-一文读懂C++11的Lambda表达式的原理与使用场景](https://zhuanlan.zhihu.com/p/717554993)

## Lambda表达式基本语法

```cpp
[capture](parameters) -> return_type { body }
```

### 捕获列表说明

- `[]` - 不捕获任何变量
- `[=]` - 按值捕获所有变量
- `[&]` - 按引用捕获所有变量
- `[x, &y]` - 按值捕获x，按引用捕获y
- `[=, &x]` - 按值捕获所有变量，但x按引用捕获
- `[&, x]` - 按引用捕获所有变量，但x按值捕获

## 使用示例

```cpp
// 简单的lambda表达式
[](int x, int y) { return x + y; }

// 带捕获的lambda
int a = 10;
[&a](int x) { return a + x; }

// 指定返回类型
[](double x) -> int { return static_cast<int>(x); }
```

## 常见使用场景

1. **STL算法** - 与std::sort, std::for_each等配合使用
2. **回调函数** - 作为函数参数传递
3. **异步编程** - 在多线程环境中使用
4. **函数对象** - 替代传统的仿函数

## 注意事项

- 注意捕获变量的生命周期
- 避免在lambda中捕获过大的对象
- 考虑性能影响，特别是按值捕获大对象时