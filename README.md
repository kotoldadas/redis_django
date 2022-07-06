# Özet
Bu uygulamada çeşitli teknolojilerin örnek bir django uygulamasına eklenme örneklerini içerir.
Kullanılan teknolojiler:
* Redis ile cache örneği
* Websocket
* RQ_Worker ile paralel hesaplama
* S3 download - upload ve zipleme işlemleri

<!-- # Kurulum -->
<!---->
<!-- Uygulamada kullanılan kütüphaneler, paralel işlemler için _fork_ fonksiyonu kullandıkları için -->
<!-- sadece Linux işletim sisteminde çalışabilmektedir. -->
<!---->
<!-- ## Sanal Ortam Kurulumu (virtualenv) -->
<!---->
<!-- Proje kaynak kodunun koşturulabilmesi için gereken kütüphaneler sanal ortama kurulmalıdır. -->
<!-- Sanal ortam oluşturmak için virtualenv kütüphanesi kullanılabilir. -->
<!---->
<!-- ``` -->
<!-- pip install virtualenv -->
<!-- ``` -->
<!---->
<!-- Sanal ortam kurulumu için -->
<!---->
<!-- ``` -->
<!-- virtualenv venv -->
<!-- ``` -->
<!---->
<!-- komutu koşturularak "venv" ismi ile bir ortam oluşturulur. -->
<!---->
<!-- ## Ortamın Aktive Edilmesi -->
<!---->
<!-- Linux işletim sistemi için -->
<!---->
<!-- ``` -->
<!-- source venv/bin/activate -->
<!-- ``` -->
<!---->
<!-- komutu koşturulur. -->
<!---->
<!-- ## Kütüphaneleri Yüklenmesi -->
<!---->
<!-- İlgili kütüphaneleri yüklemek için -->
<!---->
<!-- ``` -->
<!-- pip install -r requirements.txt -->
<!-- ``` -->
<!---->
<!-- komutu koşturulur. -->
<!---->
<!-- ## Sunucunun Ayağa Kaldırılması -->
<!---->
<!-- Projeyi ayağa kaldırmak için -->
<!---->
<!-- ``` -->
<!-- python manage.py runserver -->
<!-- ``` -->
<!---->
<!-- komutu koşturulur. -->
<!-- Bu komutu koşturmadan önce kurulan sanal ortamın aktif olduğundan ve proje dizininde bulunulduğundan emin olunmalıdır. -->
<!---->
<!-- ## Redis Kurulumu -->
<!---->
<!-- ### Local e Yüklemek -->
<!---->
<!-- Redis i yüklemek için şu komutla koşturulur. -->
<!---->
<!-- ``` -->
<!-- curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg -->
<!---->
<!-- echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list -->
<!---->
<!-- sudo apt-get update -->
<!-- sudo apt-get install redis -->
<!-- ``` -->
<!---->
<!-- Redis yüklendikten sonra arka planda çalışması için -->
<!---->
<!-- ``` -->
<!-- redis-server --daemonize yes -->
<!-- ``` -->
<!---->
<!-- ### Docker ile Redis Kurulumu -->
<!---->
<!-- ``` -->
<!-- sudo docker run --name redis_django -p 6379:6379 -d redis -->
<!-- ``` -->
<!---->
<!-- komutu koşturulur. -->
<!---->
<!-- ## Worker ların Başlatılması -->
<!---->
<!-- Uygulamadaki işlem maliyeti yüksek görevlerin paralel hesaplanmasını sağlamak için ayrı Processler (Worker) ayağa kaldırılması gerekir. Bunun için -->
<!-- ``` -->
<!-- python manage.py rqworker -->
<!-- ``` -->
<!-- komutu koşturulur. -->
<!---->
<!-- ## Test Verilerinin Yüklenmesi -->
<!---->
<!-- Uygulamadaki özelliklerin test edilmesi için hazır veriler bulunmaktadır. Bu verileri veritabanına eklemek için önce modeller veritabanında oluşturulmalıdır. Bunun için -->
<!-- ``` -->
<!-- python manage.py makemigrations -->
<!-- python manage.py migrate -->
<!-- ``` -->
<!---->
<!-- komutları koşturulur. Modeller oluştuktan sonra verileri kaydetmek için -->
<!---->
<!-- ``` -->
<!-- python manage.py loaddata cookbook -->
<!-- ``` -->
<!-- komutu koşturulur. -->
<!---->
# Docker ile Kurulumu

docker-compose ise şu komutların koşturulması yeterli olacaktır.
```
docker-compose up --build
```

Ardından admin oluşturulması için 
```
docker exec -it redis_django_web_1 bash
```

komutu ile docker container ına bağlanılır. 

```
python manage.py createsuperuser
```

komutu ile admin oluşturulur.

# Proje Mimarisi

```
.
├── Dockerfile
├── README.md                            -- Uygulama dökümanasyonunun bulunduğu dosya
├── chat                                 -- Websocket konfigürasyon dosyalarının bulunduğu klasör
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumer.py
│   ├── models.py
│   ├── routing.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── cookbook                             -- cache örneği için oluşturulan model ve view kodlarının bulunduğu klasör
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── cookbook.json
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── docker-compose.yml
├── docker-entrypoint.sh
├── dump.rdb
├── manage.py                            -- Sunucuyu ayağa kaldırma vs gibi yardımcı fonksiyonları barındıran ana script
├── nginx                                -- nginx configürasyon ve docker dosyalarının bulunduğu klasör
│   ├── Dockerfile
│   └── docking_django.conf
├── redis_tutorial                       -- Uygulamanın asıl ayarlarının bulunduğu klasör
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── storage_backends.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt                     -- Gerekli kütüphaneleri belirtildiği dosya
├── staticfiles                          -- Sunucudaki static dosyaların (css, javascript, fonts vb) bulunduğu klasör
├── students                             -- Maliyeti yüksek bir işlemi simule etmek için oluşturulan model ve fonksiyonların bulunduğu klasör
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── documents.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates                            -- html uzantılı dosyaların bulunduğu klasör
│   ├── base.html
│   ├── download.html
│   ├── index.html
│   ├── partials
│   │   ├── footer.html
│   │   └── header.html
│   ├── registration
│   │   └── login.html
│   ├── result.html
│   ├── students.html
│   ├── success.html
│   ├── test.html
│   ├── tmp.html
│   └── upload.html
└── users                                -- CustomUser modelinin ve Task modelinin bulunduğu klasör
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── manager.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

# Modeller

## Recipe - Food - Ingredient

Redis ile cache işleminin testi için oluşturulan modellerdir.

```
class Recipe(models.Model):
    """A preparation of food."""

    name = models.CharField(max_length=255)

    desc = models.TextField(null=True, blank=True)

    ingredients = models.ManyToManyField(
        "cookbook.Food",
        through="cookbook.Ingredient",
        through_fields=("recipe", "food"),
    )

    instructions = models.TextField(null=True, blank=True)

    class Meta(object):
        app_label = "cookbook"
        default_related_name = "recipes"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Food(models.Model):
    """An edible item."""

    name = models.CharField(max_length=255)

    class Meta(object):
        app_label = "cookbook"
        default_related_name = "foods"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """A food that is used in a recipe."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    # ex. 1/8 = 0.125, 1/4 = 0.250
    amount = models.DecimalField(max_digits=6, decimal_places=3, null=True, blank=True)

    # ex. tsp, tbsp, cup
    unit_of_measure = models.CharField(max_length=255)

    # ex. 2 cloves of garlic, minced
    desc = models.TextField()

    class Meta(object):
        app_label = "cookbook"

    def __unicode__(self):
        return "{recipe}: {amount} {unit_of_measure} {food}".format(
            recipe=self.recipe,
            amount=self.amount,
            unit_of_measure=self.unit_of_measure,
            food=self.food,
        )

    def __str__(self):
        return self.desc
```

## Student

Student modeli uygulama içindeki işlem maliyeti yüksek bir işlemi simule etmek için oluşturulmuştur.
Bu işlemde 10000 tane rastgele Student objesi oluşturulur.
Ardından bu objelerin id leri listede tutulur. 
Listedeki id ler döngü ile dönülerek her bir Student objesi veritabanından bulunur ve silinir.

```
class Student(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="İsim")
    last_name = models.CharField(max_length=30, verbose_name="Soy İsim")
    email = models.EmailField(
        max_length=254, verbose_name="email", default="default@test.com"
    )
    age = models.IntegerField(verbose_name="Yaş")

    def __str__(self):
        return f"name => {self.first_name}\nlast name => {self.last_name}\nage => {self.age}\nemail => {self.email}"
```

## Task

İşlem maliyeti yüksek paralel hesaplanması gereken işlemleri temsil eder.
```

class Task(models.Model):
    task_id = models.CharField(
        verbose_name="Görev ID",
        max_length=100,
        primary_key=True,
        unique=True,
        default="-1",
    )

    class StatusChoices(models.TextChoices):
        ON_PROGRESS = "ONP", "On Progress"
        FINISHED = "FNS", "Finished"

    status = models.CharField(
        verbose_name="Görev Durumu",
        choices=StatusChoices.choices,
        max_length=3,
        default=StatusChoices.ON_PROGRESS,
    )
    started = models.DateTimeField(
        auto_now_add=True, verbose_name="Görev Başlama Zamanı"
    )

    def __str__(self):
        return f"id => {self.task_id} - status => {self.status} - started => {self.started}"
```

## CustomUser

CustomUser modeli django tarafından sağlanan User modelinin modifiye edilmiş versiyonudur.
CustomUser modelinde kullanıcıların maliyeti yüksek işlemlerinin id leri de ekstra olarak tutulur

```
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email", unique=True, default="text@text.com"
    )
    channel_name = models.CharField(
        blank=True, null=True, verbose_name="kanal ismi", max_length=50
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        db_table = "custom_user"

    def __str__(self):
        return self.email  # type: ignore
```

## Document

Document modeli S3 sunucusuna yüklenen dosyaları temsil eder.

```
class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
```


# Uç Noktalar

## Sayfalar

* ``/`` cookbook verilerinin cache örneğini gösterir.
* ``/students/`` Students tablosundaki verileri gösterir.
* ``/students/test/`` İşlem maliyeti yüksek görevin başlatılmasını sağlayan butonu bulunduran sayfa.
* ``/students/test/search/<name:str>`` Öğrenci modelinde arama yapılmasını sağlayan uç nokta.
* ``/result/`` Uygulamada paralel çalışan görevlerin durumunu gösteren sayfa.
* ``/django-rq/`` Arka planda çalışan görevlerin durumunun izlenebileceği uç noktayı gösterir.
* ``/accounts/`` Uygulamadaki hesapların yönetildiği sayfayı gösterir.
* ``/core/upload/`` S3 sunucusuna dosya yüklemeyi sağlar.
* ``/core/download/`` S3 sunucunda bulunan herhangi bir klasördeki dosyaların zipleyip kullanıcıya gönderir.

```
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cookbook.urls")),
    path("students/", include("students.urls")),
    path("result/", include("users.urls")),
    path("django-rq/", include("django_rq.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("core/", include("core.urls")),
]
```

## Websocket

* ``/ws/task/`` Websocket bağlantısının kurulması için gereken uçnoktayı gösterir.

```
websocket_urlpatterns = [
    re_path(r"ws/task/", ChatConsumer.as_asgi()),
]

```

# Bazı Önemli Fonksiyonlar

## Maliyeti Yüksek Fonskiyon

```
from faker import Faker

def crud(pk_user):
    # delete all
    Student.objects.all().delete()  # type: ignore
    l = []
    fake = Faker()

    # save
    for _ in range(10000):
        # name = "".join(random.choice(letters) for _ in range(random.randint(10, 30)))
        # last_name = "".join(
        #     random.choice(letters) for _ in range(random.randint(10, 30))
        # )
        name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        age = random.randint(15, 70)
        student = Student(first_name=name, last_name=last_name, age=age, email=email)
        student.save()
        l.append(student.pk)
        print(f"{student} saved")
        sleep(0.001)
```

## Websocket Ayarları

```

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"connected user => {self.scope['user']}")
        self.user: CustomUser = self.scope["user"]
        self.user.channel_name = self.channel_name
        await sync_to_async(self.user.save)()
        print(f"users new channel name => {self.user.channel_name}")

        self.room_name = "test_room"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # type: ignore

        await self.accept()

    async def disconnect(self, code):
        self.user.channel_name = None  # type: ignore
        await sync_to_async(self.user.save)()
        print(f"users new channel name => {self.user.channel_name}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)  # type: ignore

    async def receive(self, text_data, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(  # type: ignore
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        """it is called when any group message which type propery is 'chat_message' is received"""
        message = event["message"]

        # send message to websocket

        await self.send(text_data=json.dumps({"message": message}))

    async def success_message(self, event):

        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
```

## Websocket Bağlantısının Kurulması

Websocket bağlantısının bulunduğu kod parçası _base.html_ dosyasında bulunur.
Sadece kullanıcı girişi sağlanırsa bağlantı kurulur.

```
{% if user.is_authenticated %}

<script>

    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/task/`);

    chatSocket.onopen = function(e) {
        console.log("new connection established")
    }

    chatSocket.onmessage = function (e) {
        console.log("received", e.data)
        const data = JSON.parse(e.data);
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
        window.location.pathname = '/'

    };


</script>

{% endif %}
```

## Cache Örneği

Recipe modelindeki verilerin cache den okunma örneği

```
def get_recipes():
    if "recipes" in cache:
        recipes = cache.get("recipes")
        print(f"already in cache with ttl => {cache.ttl('recipes')}")
    else:
        print("caching")
        recipes = Recipe.objects.all()  # type: ignore
        cache.set("recipes", recipes, timeout=CACHE_TTL)
    return recipes

```

## Upload

S3 sunucularına dosya yükleme örneği

```
def image_upload(request):
    if request.method == "POST":
        image_file = request.FILES["image_file"]
        document = Document(upload=image_file)
        document.save()
        image_url = document.upload.url
        return render(request, "upload.html", {"image_url": image_url})

    return render(request, "upload.html")

```

## Download

S3 sunucularındaki herhangi bir klasör içindeki bütün dosyaların ziplenip indirilme örneği

```
def download(request):
    s3 = boto3.resource(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    my_bucket = s3.Bucket(AWS_STORAGE_BUCKET_NAME)
    if request.method == "GET":
        return render(
            request,
            "download.html",
            {
                "folders": set(
                    [
                        os.path.split(obj.key)[0]
                        for obj in my_bucket.objects.all()
                        # if not str(obj.key).startswith("static")
                    ]
                )
            },
        )

    if request.method == "POST":
        # get folder name from request
        folder_name = request.POST.get("folder_name")

        response = HttpResponse(content_type="application/zip")
        with zipfile.ZipFile(response, "w") as zip_file:

            for s3_object in my_bucket.objects.all():
                path, filename = os.path.split(s3_object.key)

                if folder_name == path:
                    # create buffer to append file to zip
                    buffer = io.BytesIO()
                    # download file from s3 to buffer
                    my_bucket.download_fileobj(s3_object.key, buffer)
                    # append buffer to zip
                    zip_file.writestr(filename, buffer.getvalue())

        response["Content-Disposition"] = f"attachment; filename=result.zip"

        return response

    return redirect("main")
```

## Elasticsearch Ayarları

Elasticsearch yazılımını django uygulamamızda kullanabilmek için _settings.py_ dosyasına 
```
ELASTICSEARCH_DSL = {
    "default": {"hosts": "search:9200"},
}
```
ayarları girilir. Burada _search:9200_ kısmındaki _search_ kısmı host u belirtir. Uygulama docker-compose ile ayağa kaldırıldığı için ve Elasticsearch 'search' ismi ile ayarlandığı için _search_ oolarak girilmiştir. _9200_ kısmı ise Elasticsearch yazılımının hangi portta çalıştığını belirtir.

Students modelinde arama yapmak için şu kod parçaları yazılmıştır.

```
@registry.register_document
class StudentDocument(Document):
    class Index:

        name = "students"

        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Student

        fields = ["first_name", "last_name", "email"]

```

fields bölümünde modeldeki hangi alanlarda arama yapılacağı ve arama sonucunda ortaya çıkan dökümanlarda hangi alanların bulunacağı belirtilir.

### Arama Örneği

```
def search(req, name):
    q = Q(
        "multi_match",
        query=str(name),
        fields=["first_name", "last_name", "email"],
        fuzziness="auto",
    )
    response = StudentDocument.search().query(q).execute()

    data = {
        "success": response.success(),
        "students": [(s.first_name, s.last_name, s.email) for s in response],
    }
    return JsonResponse(data)
```
_search_ view fonksiyonu `path("search/<name>", search, name="search"),` uçnoktasına eklenmiştir.
Bu fonksiyonu kullanmak için uç noktaya `fetch` yardımı ile istek atılır.
    

```
    let tbl = document.getElementById("table")
    let input = document.getElementById("input")

    const addElements = (data) => {
        tbl.innerHTML = "";
        const success = data["success"]
        if (!success) {
            alert("wrong query!!")
            return
        }
        const arr = data["students"]

        for (let i = 0; i < arr.length; i++) {
            tbl.innerHTML += `
        <tr>
           <td>name => ${arr[i][0]} || </td>
           <td>lastname =>${arr[i][1]} || </td>
           <td> email => ${arr[i][2]}</td>
        </tr>`
        }
    }
    input.addEventListener("keyup", () => {
        if (input.value.length > 3) {
            fetch(`/students/search/${input.value}`).then(data => data.json()).then(addElements).catch(err => alert(err))
        } else {
            tbl.innerHTML = ""
        }
    })

```
