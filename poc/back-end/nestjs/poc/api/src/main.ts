import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('POC API')
    .setDescription('API description')
    .setVersion('1.0')
    .addBearerAuth()
    .build();

  app.enableCors({
    origin: '*',
    methods: 'GET,POST,PUT,DELETE,PATCH',
    credentials: true,
    allowedHeaders: 'Content-Type, Authorization',
  });

  app.useGlobalPipes(new ValidationPipe());
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);

  await app.listen(process.env.PORT ?? 8080);
}
bootstrap();
