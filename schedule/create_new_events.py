from datetime import timedelta
from copy import deepcopy

def create(eventsobj):
    new_eventsobj = []
    # 全ての登録されたスケジュールに対して以下の処理を実行する
    for event in eventsobj:
        event_origin = deepcopy(event)
        event_origin.is_repeat = False
        
        new_eventsobj.append(event_origin)
        
        
        
        if event.repeat:
            # repeat用のスケジュールの作成
            repeat_event    = deepcopy(event)
            repeat_event.is_repeat = True
            
            stop            = event.start + timedelta(days=365)
            if event.stop:
                stop        = event.stop
            
            #print(stop)
            
            #　繰り返し元のスケジュールのid
            #default_id  = str(event.id)
            #繰り返しｌスケジュール用のidを設定
            #copy_id     = 0
            
            while True:
                repeat_event.start = repeat_event.start + timedelta(days=repeat_event.repeat)
                repeat_event.end = repeat_event.end + timedelta(days=repeat_event.repeat)
                    
                if repeat_event.start > stop:
                    print("繰り返し終了")
                    break
                
                if repeat_event.is_cancel():
                    print(str(repeat_event.title)+"の予定の登録をキャンセルします")
                else:                      
                    new_eventsobj.append(deepcopy(repeat_event))
    
    return new_eventsobj