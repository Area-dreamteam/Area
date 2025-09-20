import { ApiProperty } from '@nestjs/swagger';
import { IsEmail, IsString, MinLength } from 'class-validator';

export class RegisterDto {
  @ApiProperty({
    example: 'jane.doe@example.com',
    description: 'email'
  })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'janedoe',
    description: 'username'
  })
  @IsString()
  username: string;

  @ApiProperty({
    example: 'password123',
    description: 'Password (min. 9 characters)'
  })
  @IsString()
  @MinLength(9)
  password: string;
}
