import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { isDate, IsEmail, IsString, MinLength, IsOptional } from 'class-validator';
import { Role } from '../../common/enum/role.enum'

export class UpdateUserDto {
  @ApiPropertyOptional({ example: 'jean', description: 'New username' })
  @IsOptional()
  @IsString()
  username?: string;

  @ApiProperty({
    example: 'NewVeryVeryVeryVeryVeryStrongPassword',
    description: 'New Password (min. 9 characters)',
  })
  @IsOptional()
  @IsString()
  @MinLength(9)
  password?: string;

  @ApiPropertyOptional({
    example: 'admin',
    description: 'user role'
  })
  @IsOptional()
  @IsString()
  role?: Role;
}
