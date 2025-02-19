import random

from django.utils.translation import gettext

from djf_surveys import models
from djf_surveys.models import TYPE_FIELD, Survey, Question, Answer
from djf_surveys.utils import create_star

COLORS = [
  '#5acb9d', '#55c99e', '#50c7a2', '#4bc4a6', '#46c2a9', '#41c0ad', '#3cbeb1', '#37bcb5',
  '#34bab9', '#34b7bd', '#34b4c1', '#34b2c5', '#34afc9', '#34adcd', '#34aad1', '#34a8d4',
  '#34a5d7', '#36a2db', '#399fde', '#3c9ce1', '#4099e4', '#4396e7', '#4693ea', '#4990ed',
  '#4c8df0', '#508af3', '#5386f5', '#5683f7', '#5980fa', '#5c7dfa', '#5f7afb', '#6277fc',
  '#6574fd', '#6871fd', '#6b6efd', '#6d6bfc',"RGB(204, 134, 134)",
  "RGB(134, 204, 134)","RGB(134, 134, 204)","RGB(204, 204, 134)","RGB(204, 134, 204)",
  "RGB(134, 204, 204)","RGB(184, 154, 154)","RGB(154, 184, 154)","RGB(154, 154, 184)","RGB(194, 144, 144)",
  "RGB(144, 194, 144)","RGB(144, 144, 194)","RGB(204, 174, 134)","RGB(174, 204, 134)","RGB(134, 174, 204)",
  "RGB(184, 134, 204)","RGB(134, 184, 204)","RGB(204, 134, 174)","RGB(174, 134, 204)","RGB(134, 204, 174)",
  "RGB(204, 154, 144)","RGB(154, 204, 144)","RGB(144, 154, 204)","RGB(194, 164, 144)","RGB(164, 194, 144)",
  "RGB(144, 164, 194)","RGB(204, 184, 154)","RGB(184, 204, 154)","RGB(154, 184, 204)","RGB(174, 204, 164)",
  "RGB(204, 164, 174)","RGB(164, 204, 174)","RGB(174, 174, 204)","RGB(144, 174, 194)","RGB(194, 144, 174)",
  ]


class ChartJS:
    """
    this class to generate chart https://www.chartjs.org
    """
    chart_id = ""
    chart_name = ""
    element_html = ""
    element_js = ""
    width = 400
    height = 400
    data = []
    labels = []
    colors = COLORS

    def __init__(self, chart_id: str, chart_name: str, *args, **kwargs):
        self.chart_id = f"djfChart{chart_id}"
        self.chart_name = chart_name

    def _base_element_html(self):
        self.element_html = f"""
<div class="swiper-slide sw">
    <blockquote class="p-6 border border-gray-100 rounded-lg shadow-lg bg-white">
      <canvas id="{self.chart_id}" class="canvasid" width="{self.width}" height="{self.height}"  ></canvas>
    </blocquote>
</div>
"""

    def _shake_colors(self):
        self.colors = random.choices(COLORS, k=len(self.labels))

    def _config(self):
        pass

    def _setup(self):
        pass

    def render(self):
        self._base_element_html()
        self._shake_colors()
        script = f"""
<div class="chart-container">
    <div class="chart-title-container">
        <h2>{self.chart_name}</h2>
    </div>
    {self.element_html}
</div>
<script>
{self._setup()}
{self._config()}
  const myChart{self.chart_id} = new Chart(
    document.getElementById('{self.chart_id}'),
    config{self.chart_id}
  );
</script>
"""
        return script


class ChartPie(ChartJS):
    """ this class to generate pie chart"""

    def _config(self):
        script = """
const config%s = {
  type: 'pie',
  data: data%s,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: false,
        text: '%s',
        font: {
         size:24 , 
          weight: 'bold',
          family: 'Arial, sans-serif'
        },

        padding: {
          top: 20,
          bottom: 20,
        },
        
       lineHeight: 1.5
      }
    }
  },
};
"""
        return script % (self.chart_id, self.chart_id, self.chart_name)

    def _setup(self):
        script = """
const data%s = {
  labels: %s,
  datasets: [
    {
      label: 'Dataset 1',
      data: %s,
      backgroundColor: %s
    }
  ]
};
"""
        return script % (self.chart_id, self.labels, self.data, self.colors)


class ChartBar(ChartJS):
    """ this class to generate bar chart"""

    def _config(self):
        script = """
const config%s = {
  type: 'bar',
  data: data%s,
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    },
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: '%s'
      }
    }
  },
};
"""
        return script % (self.chart_id, self.chart_id, self.chart_name)

    def _setup(self):
        script = """
const data%s = {
  labels: %s,
  datasets: [{
    data: %s,
    backgroundColor: %s,
    borderWidth: 1
  }]
};
"""
        return script % (self.chart_id, self.labels, self.data, self.colors)


class ChartBarRating(ChartBar):
    height = 200
    rate_avg = 0
    num_stars = 5

    def _base_element_html(self):
        stars = create_star(active_star=int(self.rate_avg), num_stars=self.num_stars)
        self.element_html = f"""
<div class="swiper-slide">
    <blockquote class="p-6 border border-gray-100 rounded-lg shadow-lg bg-white">
      <div class="bg-yellow-100 space-y-1 py-5 rounded-md border border-yellow-200 text-center shadow-xs mb-2">
          <h1 class="text-5xl font-semibold"> {self.rate_avg}</h1>
          <div class="flex justify-center">
              {stars}
          </div>
          <h5 class="mb-0 mt-1 text-sm"> Rate Average</h5>
      </div>
      <canvas id="{self.chart_id}" width="{self.width}" height="{self.height}"></canvas>
    </blocquote>
</div>
"""


class SummaryResponse:

    def __init__(self, survey: Survey):
        self.survey = survey

    def _process_radio_type(self, question: Question) -> str:
        pie_chart = ChartPie(chart_id=f"chartpie_{question.id}", chart_name=question.label)
        labels = question.choices.split(",")

        data = []
        for label in labels:
            clean_label = label.strip().replace(' ', '_').lower()
            count = Answer.objects.filter(question=question, value=clean_label).count()
            data.append(count)

        pie_chart.labels = labels
        pie_chart.data = data
        return pie_chart.render()

    def _process_rating_type(self, question: Question):
        if not question.choices:  # use 5 as default for backward compatibility
            question.choices = 5

        bar_chart = ChartBarRating(chart_id=f"chartbar_{question.id}", chart_name=question.label)
        bar_chart.num_stars = int(question.choices)
        labels = [str(item + 1) for item in range(int(question.choices))]

        data = []
        for label in labels:
            count = Answer.objects.filter(question=question, value=label).count()
            data.append(count)

        values_rating = Answer.objects.filter(question=question).values_list('value', flat=True)
        values_convert = [int(v) for v in values_rating]
        try:
            rating_avg = round(sum(values_convert) / len(values_convert), 1)
        except ZeroDivisionError:
            rating_avg = 0

        bar_chart.labels = labels
        bar_chart.data = data
        bar_chart.rate_avg = rating_avg
        return bar_chart.render()

    def _process_multiselect_type(self, question: Question) -> str:
        bar_chart = ChartBar(chart_id=f"barchart_{question.id}", chart_name=question.label)
        labels = question.choices.split(",")

        str_value = []
        for answer in Answer.objects.filter(question=question):
            str_value.append(answer.value)
        all_value = ",".join(str_value)
        data_value = all_value.split(",")

        data = []
        for label in labels:
            clean_label = label.strip().replace(' ', '_').lower()
            data.append(data_value.count(clean_label))

        bar_chart.labels = labels
        bar_chart.data = data
        return bar_chart.render()

    def generate(self):
        html_str = []
        for question in self.survey.questions.all():
            if question.type_field == TYPE_FIELD.radio or question.type_field == TYPE_FIELD.select:
                html_str.append(self._process_radio_type(question))
            elif question.type_field == TYPE_FIELD.multi_select:
                html_str.append(self._process_multiselect_type(question))
            elif question.type_field == TYPE_FIELD.rating:
                html_str.append(self._process_rating_type(question))
        if not html_str:
            input_types = ', '.join(str(x[1]) for x in models.Question.TYPE_FIELD if
                                    x[0] in (
                                    models.TYPE_FIELD.radio, models.TYPE_FIELD.select, models.TYPE_FIELD.multi_select,
                                    models.TYPE_FIELD.rating))
            return """
<div class="bg-yellow-100 space-y-1 py-5 rounded-md border border-yellow-200 text-center shadow-xs mb-2">
    <h1 class="text-2xl font-semibold">{}</h1>
    <h5 class="mb-0 mt-1 text-sm p-2">{}</h5>
</div>
""".format(gettext("No summary"), gettext("Summary is available only for input type: %ss") % input_types)

        return " ".join(html_str)
