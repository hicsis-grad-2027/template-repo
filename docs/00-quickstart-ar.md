# 00 — البداية السريعة

<div dir="rtl">

## الفكرة إيه؟

مشروع التخرج ده هنشتغل فيه **زي فريق حقيقي في شركة**. نفس الـ workflow اللي هتلاقيه في أول شغل ليك: كل شغلانة ليها **issue** على الـ **board**، وكل تعديل بيتعمل في **branch** صغير، وبيدخل الـ `main` عن طريق **pull request** بعد **review**.

الهدف مش إننا نصعّبها عليكم. الهدف إن في آخر السنة يبقى عندك **repo محترم تقدر تحطه في الـ CV** وتشرح فيه الـ PRs بتاعتك في الـ interview.

## الـ loop اللي هتعمله كل مرة

1. اختار **issue** من عمود **Ready** على الـ board، واعمل لنفسك **assign**، وحرّكه لـ **In progress**.
2. اعمل **branch** جديد من `main` محدّث، واسمه بالشكل ده: `feat/12-risk-endpoint` (النوع/رقم الـ issue-اسم قصير).
3. اشتغل واعمل **commits** صغيرة.
4. اعمل **push** وافتح **PR**، وفي الوصف اكتب `Closes #12`.
5. استنى الـ **CI** يبقى أخضر، وراجع الـ diff بتاعك بنفسك الأول، وبعدين دوس **Ready for review**.
6. رُد على كل comment في الـ review، صلّح أو اشرح ليه لأ.
7. بعد الـ **approve** بيتعمل **squash merge**، والـ issue بيتقفل لوحده، والكارت بيروح **Done**.

```bash
git switch main && git pull
git switch -c feat/12-risk-endpoint
# ... شغل ...
git add -p
git commit -m "feat(backend): validate bbox query params"
git push -u origin feat/12-risk-endpoint
```

## القواعد (GitHub هو اللي بيطبقها مش إحنا)

- **مفيش push مباشر على `main`**، لأي حد.
- كل PR لازم ياخد **approve** من المشرف (أو الـ code owner).
- الـ **CI** لازم يعدّي: lint و format و tests، ومفيش `.env` أو model files أو ملفات كبيرة أو secrets.
- عنوان الـ PR لازم يبقى بالشكل ده: `feat(backend): add /risk endpoint`
- الـ PR لازم يكون مربوط بـ issue: `Closes #12`

## حاجات مهمة جداً

- **الـ `.env` عمره ما يترفع على git.** لو رفعته بالغلط: **غيّر الـ key فوراً** وبلّغ المشرف. مسح الملف مش كفاية لأنه لسه موجود في الـ history.
- **الـ branch يعيش يوم لـ 3 أيام بس**، مش branch لكل واحد طول السنة.
- **الـ PR الصغير** بيتراجع أسرع وبيتعمله merge أسرع. حاول تخليه أقل من 400 سطر.
- **كارت حجمه L؟** قسّمه قبل ما تبدأ.
- **لو واقف أكتر من ساعة** اكتب في الـ issue إنت جربت إيه. السؤال بدري مهارة، مش ضعف.

## تقرا إيه بعد كده؟

| الملف | إمتى |
|---|---|
| [01-workflow.md](01-workflow.md) | قبل أول PR |
| [02-definition-of-done.md](02-definition-of-done.md) | قبل كل PR وكل milestone |
| [03-code-review.md](03-code-review.md) | قبل أول review تعمله |
| [backend/PRINCIPLES.md](../backend/PRINCIPLES.md) | قبل ما تكتب backend أو app logic |
| [ai/AI-CONCEPTS.md](../ai/AI-CONCEPTS.md) | لو المشروع فيه جزء AI |

## أول مهمة ليك

أول issue متعيّن لكل واحد فيكم: **أضف اسمك في جدول الـ Team في الـ README**، عن طريق branch و PR كاملين. الهدف إنك تجرّب الـ loop كله مرة وهي سهلة.

</div>
