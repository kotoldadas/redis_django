# Özet

Bu uygulama, django nun senkron özelliğinden dolayı hesaplama maliyeti çok olan işlemlerin redisgibi araçlar yardımı ile paralel bir şekilde işlenmesini amaçlamaktadır.
Kullanıcılar görevlerin durumunu ayrı bir sekmeden direk olarak veya konsol üzerinden websocket bağlantısı yardımı ile haberdar olabilirler.

# Kurulum

Uygulamada kullanılan kütüphaneler, paralel işlemler için _fork_ fonksiyonu kullandıkları için
sadece Linux işletim sisteminde çalışabilmektedir.

## Sanal Ortam Kurulumu (virtualenv)

Proje kaynak kodunun koşturulabilmesi için gereken kütüphaneler sanal ortama kurulmalıdır.
Sanal ortam oluşturmak için virtualenv kütüphanesi kullanılabilir.

```
pip install virtualenv
```

Sanal ortam kurulumu için

```
virtualenv venv
```

komutu koşturularak "venv" ismi ile bir ortam oluşturulur.

## Ortamın Aktive Edilmesi

Linux işletim sistemi için

```
source venv/bin/activate
```

komutu koşturulur.

## Kütüphaneleri Yüklenmesi

İlgili kütüphaneleri yüklemek için

```
pip install -r requirements.txt
```

komutu koşturulur.

## Sunucunun Ayağa Kaldırılması

Projeyi ayağa kaldırmak için

```
python manage.py runserver
```

komutu koşturulur.
Bu komutu koşturmadan önce kurulan sanal ortamın aktif olduğundan ve proje dizininde bulunulduğundan emin olunmalıdır.

## Redis Kurulumu

Redis i yüklemek için şu komutla koşturulur.

```
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```

Redis yüklendikten sonra arka planda çalışması için

```
redis-server --daemonize yes
```

komutu koşturulur.

## Worker ların Başlatılması

Uygulamadaki işlem maliyeti yüksek görevlerin paralel hesaplanmasını sağlamak için ayrı Processler (Worker) ayağa kaldırılması gerekir. Bunun için
```
python manage.py rqworker
```
komutu koşturulur.

## Test Verilerinin Yüklenmesi

Uygulamadaki özelliklerin test edilmesi için hazır veriler bulunmaktadır. Bu verileri veritabanına eklemek için önce modeller veritabanında oluşturulmalıdır. Bunun için
```
python manage.py makemigrations
python manage.py migrate
```

komutları koşturulur. Modeller oluştuktan sonra verileri kaydetmek için

```
python manage.py loaddata cookbook
```
komutu koşturulur.


# Proje Mimarisi

```
project
│
└─── chat                               -- Websocket konfigürasyon dosyalarının bulunduğu klasör
│
└─── cookbook                           -- cache örneği için oluşturulan model ve view kodlarının bulunduğu klasör
│
└─── redis_tutorial                     -- Uygulamanın asıl ayarlarının bulunduğu klasör
│
└─── staticfiles                        -- Sunucudaki static dosyaların (css, javascript, fonts vb) bulunduğu klasör
│    │
│    └─── css                           
│    └─── fonts                          
│    └─── js                            
│
└─── students                           -- Maliyeti yüksek bir işlemi simule etmek için oluşturulan model ve fonksiyonların bulunduğu klasör
│
└─── templates                          -- html uzantılı dosyaların bulunduğu klasör
│
└─── users                              -- CustomUser modelinin ve Task modelinin bulunduğu klasör
│
│   README.md                           -- Uygulama dökümanasyonunun bulunduğu dosya
│   requirements.txt                    -- Gerekli kütüphaneleri belirtildiği dosya
│   manage.py                           -- Sunucuyu ayağa kaldırma vs gibi yardımcı fonksiyonları barındıran ana script
│   .gitignore                          -- git tarafından takip edilmemesi istenen dosya ve klasörlerin belirtildiği dosya
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

UserAnswer modeli kullanıcıyı sorulan sorular sonucunda verdiği cevapları temsil eder.
Student modeli uygulama içindeki işlem maliyeti yüksek bir işlemi simule etmek için oluşturulmuştur.
Bu işlemde 1000 tane rastgele Student objesi oluşturulur.
Ardından bu objelerin id leri listede tutulur. 
Listedeki id ler döngü ile dönülerek her bir Student objesi veritabanından bulunur ve silinir.

```
class Student(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="İsim")
    last_name = models.CharField(max_length=30, verbose_name="Soy İsim")
    age = models.IntegerField(verbose_name="Yaş")

    def __str__(self):
        return f"name => {self.first_name} - last name => {self.last_name} - age => {self.age}"
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


# Uç Noktalar

## Sayfalar
Uygulamada 2 ana uç nokta bulunmaktadır.

* ``/`` cookbook verilerinin cache örneğini gösterir.
* ``/students/`` Students tablosundaki verileri gösterir.
* ``/students/test/`` İşlem maliyeti yüksek görevin başlatılmasını sağlayan butonu bulunduran sayfa.
* ``/result/`` Uygulamada paralel çalışan görevlerin durumunu gösteren sayfa.
* ``/django-rq/`` Arka planda çalışan görevlerin durumunun izlenebileceği uç noktayı gösterir.
* ``/accounts/`` Uygulamadaki hesapların yönetildiği sayfayı gösterir.

```
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cookbook.urls")),
    path("students/", include("students.urls")),
    path("result/", include("users.urls")),
    path("django-rq/", include("django_rq.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
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
def crud(pk_user):
    # delete all
    Student.objects.all().delete()  # type: ignore
    l = []

    # save
    letters = string.ascii_lowercase
    for _ in range(1000):
        name = "".join(random.choice(letters) for _ in range(random.randint(4, 10)))
        last_name = "".join(
            random.choice(letters) for _ in range(random.randint(4, 10))
        )
        age = random.randint(15, 70)
        student = Student(first_name=name, last_name=last_name, age=age)
        student.save()
        l.append(student.pk)
        print(f"{student} saved")
        sleep(0.001)

    for pk in l:
        s = Student.objects.get(pk=pk)  # type: ignore
        s.delete()
        print(f"{s} deleted")
        sleep(0.001)

    channel_layer = get_channel_layer()
    user = CustomUser.objects.get(pk=pk_user)
    channel_name = user.channel_name
    async_to_sync(channel_layer.send)(  # type: ignore
        channel_name, {"type": "success_message", "message": "task is done"}
    )
    job: Job = rq.get_current_job()  # type: ignore
    task: Task = Task.objects.get(pk=job.id)  # type: ignore
    task.status = task.StatusChoices.FINISHED  # type: ignore
    task.save()

    print(f"fetched task => {task}")
    print(f"current job => {job}")
    print(f"user => {user}")

    return f"{user} - {job} - {task}"
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


