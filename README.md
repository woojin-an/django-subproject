# django-subproject
* 프로젝트 루트 디렉터리 생성 -> 가상환경 설정 -> 장고 설치 -> 장고 프로젝트 구성 -> 
settings의 배포/로컬 분리(base, local, prod)

---
serializers.py  
```
class serializer(ModelSerializer):
    class Meta:
        fields = '__all__' 
```
'__all__' 은 모든 필드를 가져옴

---
`models.py`
```angular2html
USERNAME_FIELD = 'email'
```

email을 유저네임으로 가져오겠다는 선언

---

```angular2html
class SignUpView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer
    
    def perform_create      # 이메일 인증을 위한 메서드 오버라이딩
        signer = TimestampSigner()      # 서명 기능 제공, secret_key 를 가지고 특정값을 암호화
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)
```

---

