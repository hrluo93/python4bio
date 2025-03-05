#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def sort_paml_interleaved(input_file, output_file=None):
    """
    将 PAML 交错格式的序列按名称字母顺序排序，
    并将结果以顺序格式(sequential)写到 output_file。
    """
    if output_file is None:
        output_file = input_file + ".sorted"  # 默认输出改名

    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # 第 1 行：N 和 L
    first_line = lines[0].strip()
    N, L = map(int, first_line.split())
    
    # 从第 2 行开始解析交错块
    # 目标：为每个物种名收集完整长度 L 的序列。
    species_names = []
    seq_dict = {}  # { species_name: sequence_so_far }
    
    # 当前读到的总行索引
    current_line_index = 1
    
    # 1) 先读入“第一块”：应包含 N 行，每行【物种名 + 序列片段】
    for i in range(N):
        line = lines[current_line_index].strip()
        current_line_index += 1
        
        # 如果行里是 "SpeciesA   ATCGAT" 这种形式
        # 简单用 split 拆分，假设第一个非空部分是物种名，剩下的是序列
        # 注意：有时物种名可能带空格，需要更精细的处理。本示例简单处理。
        parts = line.split()
        if len(parts) < 2:
            # 可能行不够，或格式有问题
            raise ValueError(f"检测到第 {current_line_index} 行格式异常：'{line}'")
        
        name = parts[0]
        seq_part = "".join(parts[1:])  # 合并剩余部分为序列
        species_names.append(name)
        seq_dict[name] = seq_part  # 初始化字典

    # 2) 后续“块”，一般只含序列片段（或者在物种名位置是空格）
    #    需要循环读取，直到每个物种序列长度 >= L
    #    每个块包含 N 行，与物种顺序一一对应
    while True:
        # 判断是否所有物种序列都达到了长度 L
        all_done = all(len(seq_dict[name]) >= L for name in species_names)
        if all_done:
            break
        
        # 如果还没到 L，则继续读 N 行
        # 需要考虑文件里可能有空行分隔块，所以要先跳过空行
        while current_line_index < len(lines) and not lines[current_line_index].strip():
            current_line_index += 1
        if current_line_index >= len(lines):
            # 文件意外结束
            break
        
        for i in range(N):
            if current_line_index >= len(lines):
                break
            line = lines[current_line_index].strip()
            current_line_index += 1
            
            if not line:
                # 遇到空行，可能需要跳过，然后下一个块再继续
                continue
            
            parts = line.split()
            if len(parts) == 0:
                # 全空格或空行
                continue
            
            # 在交错格式的后续块中，物种名列通常是空或者很短
            # 根据行次 i 来对应 species_names[i]，再拼接序列即可
            seq_part = "".join(parts[-1:])  # 最后一个部分视为序列段
            sp_name = species_names[i]
            seq_dict[sp_name] += seq_part

    # 3) 如果某些物种的序列没拼齐到 L 长度，说明文件中可能还缺块
    for sp in seq_dict:
        if len(seq_dict[sp]) < L:
            print(f"[警告] 物种 {sp} 序列长度只有 {len(seq_dict[sp])}，未达到设定 {L}")

    # 4) 按物种名称排序
    sorted_items = sorted(seq_dict.items(), key=lambda x: x[0])

    # 5) 写出结果（这里写成顺序格式）
    with open(output_file, 'w') as out:
        out.write(f"{N} {L}\n")
        for name, seq in sorted_items:
            # 若序列过长或有额外拼接错误，需要检查
            seq = seq[:L]  # 截断到 L，防止多余
            out.write(f"{name}\n{seq}\n")

    print(f"[完成] 交错格式排序写出：{output_file}")

def main():
    if len(sys.argv) < 2:
        print("用法：python sort_paml_interleaved.py input.phy [output.phy]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    sort_paml_interleaved(input_file, output_file)

if __name__ == "__main__":
    main()
