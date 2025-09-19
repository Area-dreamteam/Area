import { ApiProperty } from '@nestjs/swagger';
import { isDate, IsEmail, IsString, MinLength, IsOptional } from 'class-validator';
import { Role } from '../../common/enum/role.enum'

export class CreateUserDto {
  @ApiProperty({ example: 'jean', description: 'username' })
  @IsString()
  username: string;

  @ApiProperty({
    example: 'NewVeryVeryVeryVeryVeryStrongPassword',
    description: 'Password (min. 9 characters)',
  })
  @IsString()
  @MinLength(9)
  password: string;

  @ApiProperty({
    example: 'user',
    description: 'Role of user',
    required: false
  })
  @IsOptional()
  @IsString()
  role?: Role;
}
