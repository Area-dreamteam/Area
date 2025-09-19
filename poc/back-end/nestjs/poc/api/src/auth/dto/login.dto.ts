import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsString } from 'class-validator';

export class LoginDto {
  @ApiProperty({ example: 'jane.doe@example.com', description: 'login email' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'password123', description: 'login password' })
  @IsString()
  password: string;
}
