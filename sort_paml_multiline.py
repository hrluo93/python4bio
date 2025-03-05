#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def sort_paml_multiline(input_file, output_file=None):
    """
    读取 '顺序格式 + 多行序列' 的 PAML/PHYLIP 文件，
    将每个物种序列拼成一行，然后按物种名排序，写出到 output_file（顺序格式）。
    """
    if output_file is None:
        output_file = input_file + ".sorted"
    
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    # 第1行: N(物种数), L(序列长度)
    first_line = lines[0].strip()
    N, L = map(int, first_line.split())
    
    # 准备一个字典存放 {species_name: sequence_str}
    seq_dict = {}
    
    current_line_index = 1  # 从第2行开始
    for i in range(N):
        # 1) 读物种名称（跳过空行等）
        while not lines[current_line_index].strip():
            current_line_index += 1
        species_name = lines[current_line_index].strip()
        current_line_index += 1
        
        # 2) 读物种序列，多行拼接
        seq_fragments = []
        current_seq_length = 0
        
        while current_seq_length < L:
            if current_line_index >= len(lines):
                # 文件不够，报错或警告
                raise ValueError(f"文件数据不足，{species_name} 的序列尚未达到长度 {L}")
            line_seq = lines[current_line_index].strip()
            current_line_index += 1
            
            # 如果行是空行，可能需要跳过继续读下一行
            if not line_seq:
                continue
            
            # 拼接
            seq_fragments.append(line_seq)
            current_seq_length += len(line_seq)
        
        full_sequence = "".join(seq_fragments)
        # 如果多读了长度 > L，可以在此做截断 full_sequence = full_sequence[:L]
        if len(full_sequence) > L:
            full_sequence = full_sequence[:L]
        
        seq_dict[species_name] = full_sequence
    
    # 对物种名称进行字母顺序排序
    sorted_items = sorted(seq_dict.items(), key=lambda x: x[0])
    
    # 写出结果：顺序格式(sequential)，每条序列只占 2 行（名称 + 序列）
    with open(output_file, 'w') as out:
        out.write(f"{N} {L}\n")
        for name, seq in sorted_items:
            out.write(f"{name}\n{seq}\n")
    
    print(f"[完成] 已处理多行序列并按名称排序写至：{output_file}")

def main():
    if len(sys.argv) < 2:
        print("用法：python sort_paml_multiline.py input.phy [output.phy]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    sort_paml_multiline(input_file, output_file)

if __name__ == "__main__":
    main()
