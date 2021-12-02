import json
import os
import threading
import xml.dom.minidom


from interface_app.apps import RUN_TASK_FILE, TASK_DIR
from interface_app.models import Testtask, Testcase, Taskresult


class ThreadTask:
    def __init__(self, task_id):
        self.tid = task_id

    def run_task(self):
        task_obj = Testtask.objects.get(id=self.tid)
        cases = task_obj.cases
        cases = cases.split(',')
        cases.pop()
        task_obj.status = 1  # 任务状态变成运行中
        task_obj.save()
        cases_dict = {}
        for case in cases:
            case_obj = Testcase.objects.get(id=case)
            case_info = {'url': case_obj.req_url, 'method': case_obj.req_method, 'ptype': case_obj.req_ptype,
                         'header': case_obj.req_header, 'parameter': case_obj.req_parameter,
                         'assert_': case_obj.res_assert}
            cases_dict[case] = case_info
        case_str = json.dumps(cases_dict)
        task_dir = TASK_DIR
        with open(task_dir + 'cases_data.json', 'w') as f:
            f.write(case_str)
        os.system(
            'python3 ' + RUN_TASK_FILE
        )

    def save_result(self):
        '''
        保存运行结果
        '''
        # 打开xml文档
        dom = xml.dom.minidom.parse(TASK_DIR + 'results.xml')
        # 得到文档元素对象
        root = dom.documentElement
        ts = root.getElementsByTagName('testsuite')
        name = ts[0].getAttribute("name")
        tests = ts[0].getAttribute("tests")
        failures = ts[0].getAttribute("failures")
        skipped = ts[0].getAttribute("skipped")
        errors = ts[0].getAttribute("errors")
        time = ts[0].getAttribute("time")
        timestamp = ts[0].getAttribute("timestamp")

        with open(TASK_DIR + 'results.xml', 'r', encoding='utf-8') as f:
            result_text = f.read()
        Taskresult.objects.create(task_id=self.tid, name=name, tests=tests, failures=failures,skipped=skipped,
                                  errors=errors, time=time, result=result_text, run_time=timestamp)

    def run_thr(self):
        threads = []
        t = threading.Thread(target=self.run_task)
        threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print('执行(任务)线程之后的动作。。。。')

        self.save_result()
        task_obj = Testtask.objects.get(id=self.tid)
        task_obj.status = 2  # 任务状态变成已执行
        task_obj.save()

    def run(self):
        threads = []
        r = threading.Thread(target=self.run_thr)
        threads.append(r)
        for r in threads:
            r.start()
