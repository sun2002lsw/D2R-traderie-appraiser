import os
import json


def build_html(value_data):
    trade_times, item_value_data_for_chart = refine_data(value_data)

    # JSON 문자열로 변환
    trade_times_str = json.dumps(trade_times)
    softcore_ladder_str = json.dumps(item_value_data_for_chart['Softcore_Ladder'])
    softcore_non_ladder_str = json.dumps(item_value_data_for_chart['Softcore_NonLadder'])
    hardcore_ladder_str = json.dumps(item_value_data_for_chart['Hardcore_Ladder'])

    # HTML 템플릿 파일 경로 처리
    current_code_path = os.path.abspath(__file__)
    current_directory_path = os.path.dirname(current_code_path)
    template_file_path = os.path.join(current_directory_path, 'html_template.txt')
    with open(template_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 템플릿 내에 데이터를 대체
    content = (content.replace('placeholder_Trade_Times', trade_times_str)
               .replace('placeholder_Softcore_Ladder_Values', softcore_ladder_str)
               .replace('placeholder_Softcore_NonLadder_Values', softcore_non_ladder_str)
               .replace('placeholder_Hardcore_Ladder_Values', hardcore_ladder_str))

    return content


def refine_data(value_data):
    trade_times = sorted({data['Time'] for data in value_data})

    # 데이터 추출
    item_value_data = {}
    for data in value_data:
        data_type = data['Type']
        trade_time = data['Time']
        item_values = json.loads(data['ItemValues'])

        if data_type not in item_value_data:
            item_value_data[data_type] = {}

        for trade_item, item_value in item_values.items():
            if trade_item == 'Perfect Amethyst':
                continue # 퍼자의 가격은 항상 1이라서 의미 없다
            if trade_item not in item_value_data[data_type]:
                item_value_data[data_type][trade_item] = {}
            item_value_data[data_type][trade_item][trade_time] = item_value

    # 시간별 가치를 배열로 변환
    item_value_data_for_chart = {}
    for data_type, items in item_value_data.items():
        item_value_data_for_chart[data_type] = {}

        for trade_item, values_by_time in items.items():
            item_values = []
            previous_value = 0  # 가치 정보가 없는 시간은 이전 시간의 가치를 그대로 계승
            
            for trade_time in trade_times:
                current_value = values_by_time.get(trade_time, previous_value)
                
                item_values.append(current_value)
                previous_value = current_value

            item_value_data_for_chart[data_type][trade_item] = item_values

    return trade_times, item_value_data_for_chart
